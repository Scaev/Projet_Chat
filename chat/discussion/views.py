# -*- coding: utf-8 -*-
from discussion.forms import ConnexionForm,InscriptionForm,ChangementForm,EnvoiMessage,AjoutAmiForm
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect,render,render_to_response
from models import Utilisateur,Conversation,Message
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import get_object_or_404
import hashlib

# render_to_response est utilisé pour l'affichage des erreurs dans les formulaires.
# de même pour RequestContext



def connexion(request):
    
    if request.method == 'POST':  # S'il s'agit d'une requête POST
        form = ConnexionForm(request.POST)  # Nous reprenons les données
            
        if form.is_valid(): # Nous vérifions que les données envoyées sont valides
            
            # Ici nous pouvons traiter les données du formulaire
            
            identifiant=form.clean_identifiant()
            mdp=form.clean_mdp()
            for utilisateur in Utilisateur.objects.all():
                if identifiant==utilisateur.pseudo or identifiant==utilisateur.telephone or identifiant==utilisateur.email:
                    compte=utilisateur
	            
            return HttpResponseRedirect(reverse('discussion.views.conversations',args=[compte]))
                    
    # rajouter deux liens: un pour retourner sur la page de connexion , l autre pour changer de mdp
        
        else:
            return render_to_response('discussion/connexion.html', { 'form': form, },context_instance=RequestContext(request))
    else: # Si ce n'est pas du POST, c'est probablement une requête GET
        form = ConnexionForm()  # Nous créons un formulaire vide
        return render(request, 'discussion/connexion.html',locals())

def conversations(request,pseudo_utilisateur):
    utilisateur=get_object_or_404(Utilisateur,pseudo=pseudo_utilisateur)
    conversations=utilisateur.conversations.all()
    for conversation in conversations:
        if conversation.participants.count()<2:
            conversation.delete()
    conversations=utilisateur.conversations.all()
    return render(request,'discussion/conversations.html',{'conversations':conversations,'utilisateur':utilisateur})

def creation_nouvelle_conversation(request,pseudo_utilisateur):    
    utilisateur=get_object_or_404(Utilisateur,pseudo=pseudo_utilisateur)
    nouvelle_conversation=Conversation()
    nouvelle_conversation.save()
    nouvelle_conversation.participants.add(utilisateur)
    return render(request,'discussion/creation_conversation.html',{'utilisateur':utilisateur})

def creation_conversation(request,pseudo_utilisateur):
    utilisateur=get_object_or_404(Utilisateur,pseudo=pseudo_utilisateur)
    return render(request,'discussion/creation_conversation.html',{'utilisateur':utilisateur})

def ajout_ami_creation_conversation(request,pseudo_utilisateur):
    if request.method == 'POST':  # S'il s'agit d'une requête POST
        form = AjoutAmiForm(request.POST)  # Nous reprenons les données
            
        if form.is_valid(): # Nous vérifions que les données envoyées sont valides    
            pseudo_ami=form.cleaned_data['pseudo_ami']
            
            utilisateur=get_object_or_404(Utilisateur,pseudo=pseudo_utilisateur)
            ami=get_object_or_404(Utilisateur,pseudo=pseudo_ami) #verifie que l'ami existe effectivement
            conversation=utilisateur.conversations.all().last() #appelle la dernière conversation créée
            conversation.participants.add(ami) #ajoute l'ami à la conversation
            
            return HttpResponseRedirect(reverse('discussion.views.creation_conversation',kwargs={'pseudo_utilisateur':pseudo_utilisateur}))
        else:
            return HttpResponseRedirect(reverse('discussion.views.creation_conversation',kwargs={'pseudo_utilisateur':pseudo_utilisateur}))  
    else:
        form=AjoutAmiForm()
        return HttpResponse("Erreur, veuillez recommencer svp")

def quitter_conversation(request,pseudo_utilisateur,id_conversation):
    utilisateur=Utilisateur.objects.get(pseudo=pseudo_utilisateur)
    conversation=Conversation.objects.get(id=id_conversation)
    conversation.participants.remove(utilisateur)
    if conversation.participants.count()<2: #s'il ne reste qu'une personne dans la conversation, celle-ci est supprimée
        conversation.delete()
    conversations=utilisateur.conversations.all()
    return HttpResponseRedirect(reverse('discussion.views.conversations',kwargs={'pseudo_utilisateur':pseudo_utilisateur}))
    #return render(request, 'discussion/conversations.html',{'conversations':conversations,'utilisateur':utilisateur})

def ajout_ami_conversation(request,pseudo_utilisateur,id_conversation):
    
    if request.method=='POST':  
        
        form=AjoutAmiForm(request.POST)
        compte=Utilisateur.objects.get(pseudo=pseudo_utilisateur)
        conversations=compte.conversations.all()
        if form.is_valid():
            pseudo_ami=form.cleaned_data['pseudo_ami']
            if pseudo_ami==pseudo_utilisateur: #verification que l'utilisateur n'a pas entré son propre pseudo
                return HttpResponseRedirect(reverse('discussion.views.conversations',args=[compte]))            
            else:                
                ami=get_object_or_404(Utilisateur,pseudo=pseudo_ami) #on verifie si le pseudo de l'ami existe              
                conversation=Conversation.objects.get(id=id_conversation) #on récupère la conversation dans la base de donnée
                if ami in conversation.participants.all(): #on vérifie que l'ami ne soit pas deja dans la conversation
                    return HttpResponseRedirect(reverse('discussion.views.conversations',args=[compte]))
                else:
                    conversation.participants.add(ami) #on ajoute l'ami à la conversation                       
                    return HttpResponseRedirect(reverse('discussion.views.conversations',args=[compte])) 
        else:           
            return HttpResponseRedirect(reverse('discussion.views.conversations',args=[compte]))
    else:
        
        form=AjoutAmiForm()
        
        return HttpResponseRedirect(reverse('discussion.views.conversations',args=[compte]))
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
	    mot_de_passe_hash = hashlib.md5()
	    mot_de_passe = "cHa473s" + mot_de_passe + "40b1";
	    mot_de_passe_hash.update(mot_de_passe)
            user=Utilisateur(pseudo=pseudo,mot_de_passe=mot_de_passe_hash.hexdigest(),telephone=telephone,email=email)
            user.save()
            return HttpResponseRedirect(reverse('discussion.views.conversations',args=[user]))
        else:
            
            return render_to_response('discussion/inscription.html', { 'form': form, },context_instance=RequestContext(request))
    else: # Si ce n'est pas du POST, c'est probablement une requête GET
        form = InscriptionForm()  # Nous créons un formulaire vide
        return render(request, 'discussion/inscription.html', locals())

def conversation(request,pseudo_utilisateur, id_conversation):
    utilisateur=Utilisateur.objects.get(pseudo=pseudo_utilisateur)    

    return render(request, 'discussion/conversation.html', locals())

def affichageMessage(request, pseudo_utilisateur, id_conversation):
    conversation_courante=Conversation.objects.get(id=id_conversation)    

    utilisateur=Utilisateur.objects.get(pseudo=pseudo_utilisateur)
    return render(request, 'discussion/affichageMessage.html', locals())

def envoiMessage(request, pseudo_utilisateur, id_conversation):
    conversation_courante=Conversation.objects.get(id=id_conversation)    

    utilisateur=Utilisateur.objects.get(pseudo=pseudo_utilisateur)

    if request.method == 'POST':  # S'il s'agit d'une requête POST
        form = EnvoiMessage(request.POST)  # Nous reprenons les données
        
        if form.is_valid(): # Nous vérifions que les données envoyées sont valides
            
            # Ici nous pouvons traiter les données du formulaire
            texte = form.cleaned_data['texte']
            
           
            texte = texte.replace('stupide', '** gentil **')
            texte = texte.replace('cretin', '** chenapan **')
            texte = texte.replace('merde', '** zut **')
            texte = texte.replace('moche', '** beau **')
            
            
 
            message=Message(auteur = utilisateur ,texte = texte)            
            message.save()
            form = EnvoiMessage()
	    conversation_courante.messages.add(message)

    else: # Si ce n'est pas du POST, c'est probablement une requête GET
        form = EnvoiMessage()  # Nous créons un formulaire vide
    	
    return render(request, 'discussion/envoiMessage.html', locals())

def changement(request):
    if request.method == 'POST':  # S'il s'agit d'une requête POST
        form = ChangementForm(request.POST)  # Nous reprenons les données
        
        if form.is_valid(): # Nous vérifions que les données envoyées sont valides
            
            
            utilisateur_pseudo=form.cleaned_data['pseudo']
            
            nouveau_mot_de_passe=form.cleaned_data['mdp']
            nouveau_mot_de_passe_hash = hashlib.md5()
            nouveau_mot_de_passe = "cHa473s" + nouveau_mot_de_passe + "40b1";
            nouveau_mot_de_passe_hash.update(nouveau_mot_de_passe)
            
            utilisateur=Utilisateur.objects.get(pseudo=utilisateur_pseudo)
            utilisateur.mot_de_passe=nouveau_mot_de_passe_hash.hexdigest()
            utilisateur.save()
            return  HttpResponseRedirect(reverse('discussion.views.conversations',args=[utilisateur]))
            
            
        else:
        
            return render_to_response('discussion/changement.html', { 'form': form, },context_instance=RequestContext(request))
    else: # Si ce n'est pas du POST, c'est probablement une requête GET
        form = ChangementForm()  # Nous créons un formulaire vide
        return render(request, 'discussion/changement.html', locals())



    	

