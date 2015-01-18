# -*- coding: utf-8 -*-
from discussion.forms import ConversationCreationForm,ConnexionForm, InscriptionForm,ChangementForm, EnvoiMessage
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect,render,render_to_response
from models import Utilisateur,Conversation,Message#,EnvoiMessage
from django.core.urlresolvers import reverse
from django.template import RequestContext
# render_to_response est utilisé pour l'affichage des erreurs dans les formulaires.
# de même pour RequestContext


def connexion(request):
    
    if request.method == 'POST':  # S'il s'agit d'une requête POST
        form = ConnexionForm(request.POST)  # Nous reprenons les données
            
        if form.is_valid(): # Nous vérifions que les données envoyées sont valides
            
            # Ici nous pouvons traiter les données du formulaire
            identifiant = form.cleaned_data['identifiant']
            mot_de_passe = form.cleaned_data['mdp']
            #user=Utilisateur(pseudo=pseudo,mot_de_passe=mot_de_passe)
            
            for utilisateur in Utilisateur.objects.all():
                if identifiant==utilisateur.pseudo or identifiant==utilisateur.telephone or identifiant==utilisateur.email:
                    if mot_de_passe== utilisateur.mot_de_passe:
                        #return HttpResponseRedirect(reverse('conversations',kwargs={'utilisateur':user})) 
                        #return redirect('conversations',user='utilisateur')
                        return HttpResponseRedirect(reverse('discussion.views.conversations',args=[utilisateur]))
                    else:
                        return HttpResponse('Le compte existe bien mais le mot de passe est erroné, essaie encore! :)')
            return HttpResponse('compte non existant, verifiez pseudo')
        else:
            return render_to_response('discussion/connexion.html', { 'form': form, },context_instance=RequestContext(request))
    else: # Si ce n'est pas du POST, c'est probablement une requête GET
        form = ConnexionForm()  # Nous créons un formulaire vide
        return render(request, 'discussion/connexion.html',locals())

def conversations(request,pseudo_utilisateur):
    try:
        utilisateur=Utilisateur.objects.get(pseudo=pseudo_utilisateur)
        conversations=utilisateur.conversations.all()
        return render(request,'discussion/conversations.html',{'conversations':conversations,'utilisateur':utilisateur})
    except Utilisateur.DoesNotExist:
        return HttpResponse('Erreur')


def creation_conversation(request,pseudo_utilisateur):	
    if request.method=='POST':        
        form=ConversationCreationForm(request.POST)        
        if form.is_valid():
            pseudo_ami=form.cleaned_data['pseudo_ami']
            if pseudo_ami==pseudo_utilisateur: #verification que l'utilisateur n'a pas entré son propre pseudo
                return HttpResponse('Le pseudo de votre ami doit être différent du vôtre !')            

            try:
                utilisateur=Utilisateur.objects.get(pseudo=pseudo_utilisateur)
                ami=Utilisateur.objects.get(pseudo=pseudo_ami) #on verifie si ce pseudo existe dans la base de donnée                
                nouvelle_conversation=Conversation() #on crée la conversation
                nouvelle_conversation.save() 
                nouvelle_conversation.participants.add(utilisateur,ami) #on ajoute l'ami et l'utilisateur à la conversation                       
                return render(request, 'discussion/creation_conversation.html',{'utilisateur':utilisateur})
            except Utilisateur.DoesNotExist:
                return HttpResponse("""Ce pseudo n'existe pas!""")  # s'il n'existe pas -> message d'erreur 
        else:
            return HttpResponse("Erreur, formulaire non valide")             
    else:
        form=ConversationCreationForm()
        return HttpResponse("Erreur, veuillez recommencer svp")

def quitter_conversation(request,pseudo_utilisateur,id_conversation):
    utilisateur=Utilisateur.objects.get(pseudo=pseudo_utilisateur)
    conversation=Conversation.objects.get(id=id_conversation)
    conversation.participants.remove(utilisateur)
    if conversation.participants.count()<2: #s'il ne reste qu'une personne dans la conversation, celle-ci est supprimée
        conversation.delete()
    return render(request, 'discussion/quitter_conversation.html',{'utilisateur':utilisateur})

def ajout_ami_conversation(request,pseudo_utilisateur,id_conversation):	
    if request.method=='POST':        
        form=ConversationCreationForm(request.POST)        
        if form.is_valid():
            pseudo_ami=form.cleaned_data['pseudo_ami']
            if pseudo_ami==pseudo_utilisateur: #verification que l'utilisateur n'a pas entré son propre pseudo
                return HttpResponse('Le pseudo de votre ami doit être différent du vôtre !')            
            try:
                utilisateur=Utilisateur.objects.get(pseudo=pseudo_utilisateur)
                ami=Utilisateur.objects.get(pseudo=pseudo_ami) #on verifie si ce pseudo existe dans la base de donnée                
                conversation=Conversation.objects.get(id=id_conversation) #on récupère la conversation dans la base de donnée
                if ami in conversation.participants.all():
                    return HttpResponse('Cette personne appartient déjà à la conversation!')
                else:
                    conversation.participants.add(ami) #on ajoute l'ami à la conversation                       
                    return render(request, 'discussion/ajout_ami_conversation.html',{'utilisateur':utilisateur})
            except Utilisateur.DoesNotExist:
                return HttpResponse("""Ce pseudo n'existe pas!""")  # s'il n'existe pas -> message d'erreur 
        else:
            return HttpResponse("Erreur, formulaire non valide")             
    else:
        form=ConversationCreationForm()
        return HttpResponse("Erreur, veuillez recommencer svp")

def inscription(request):
    if request.method == 'POST':  # S'il s'agit d'une requête POST
        form = InscriptionForm(request.POST)  # Nous reprenons les données
        
        if form.is_valid(): # Nous vérifions que les données envoyées sont valides
            
            # Ici nous pouvons traiter les données du formulaire
            pseudo = form.cleaned_data['pseudo']
            mot_de_passe = form.cleaned_data['mdp']
            telephone=form.cleaned_data['telephone']
            email=form.cleaned_data['email']
            user=Utilisateur(pseudo=pseudo,mot_de_passe=mot_de_passe,telephone=telephone,email=email)
            user.save()
            return HttpResponseRedirect(reverse('discussion.views.conversations',args=[user]))
        else:
            
            return render_to_response('discussion/inscription.html', { 'form': form, },context_instance=RequestContext(request))
    else: # Si ce n'est pas du POST, c'est probablement une requête GET
        form = InscriptionForm()  # Nous créons un formulaire vide
        return render(request, 'discussion/inscription.html', locals())

def conversation(request,id_conversation, pseudo_utilisateur):
    #  conversation_courante = Conversation()
    # conversation_courante.save()
    utilisateur=Utilisateur.objects.get(pseudo=pseudo_utilisateur)

    if request.method == 'POST':  # S'il s'agit d'une requête POST
        form = EnvoiMessage(request.POST)  # Nous reprenons les données
        
        if form.is_valid(): # Nous vérifions que les données envoyées sont valides
            
            # Ici nous pouvons traiter les données du formulaire
            texte = form.cleaned_data['texte']
            auteur = form.cleaned_data['auteur']
            message=Message(auteur = auteur ,texte = texte)            
            message.save()

    else: # Si ce n'est pas du POST, c'est probablement une requête GET
        form = EnvoiMessage()  # Nous créons un formulaire vide
    
    #conversation_courante.messages.add(message)
    messages = Message.objects.all()
    #messages=conversation_courante.messages

    return render(request, 'discussion/conversation.html', locals())

def changement(request):
    if request.method == 'POST':  # S'il s'agit d'une requête POST
        form = ChangementForm(request.POST)  # Nous reprenons les données
        
        if form.is_valid(): # Nous vérifions que les données envoyées sont valides
            
            
            utilisateur_pseudo=form.cleaned_data['pseudo']
            utilisateur_email=form.cleaned_data['email']
            utilisateur_telephone=form.cleaned_data['telephone']
            nouveau_mot_de_passe = form.cleaned_data['mdp']
            
            if utilisateur_pseudo==utilisateur_email==utilisateur_telephone:
                
                utilisateur=Utilisateur.objects.get(pseudo=utilisateur_pseudo)
                utilisateur.mot_de_passe=nouveau_mot_de_passe
                utilisateur.save()
                return  HttpResponseRedirect(reverse('discussion.views.conversations',args=[utilisateur]))
            
            else:
                return HttpResponse('Probleme dans les identifiants donnés')
        else:
        
            return render_to_response('discussion/changement.html', { 'form': form, },context_instance=RequestContext(request))
    else: # Si ce n'est pas du POST, c'est probablement une requête GET
        form = ChangementForm()  # Nous créons un formulaire vide
        return render(request, 'discussion/changement.html', locals())

