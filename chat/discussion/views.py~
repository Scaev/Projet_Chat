# -*- coding: utf-8 -*-
from discussion.forms import UserForm,ConversationCreationForm
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect,render
from models import Utilisateur,Conversation,Message
from django.core.urlresolvers import reverse



def connexion(request):
    
    if request.method == 'POST':  # S'il s'agit d'une requête POST
        form = UserForm(request.POST)  # Nous reprenons les données
        
        if form.is_valid(): # Nous vérifions que les données envoyées sont valides
            existant=False;
            # Ici nous pouvons traiter les données du formulaire
            pseudo = form.cleaned_data['pseudo']
            mot_de_passe = form.cleaned_data['mdp']
            user=Utilisateur(pseudo=pseudo,mot_de_passe=mot_de_passe)
            
            for utilisateur in Utilisateur.objects.all():
                if user.pseudo==utilisateur.pseudo:
                    if user.mot_de_passe== utilisateur.mot_de_passe:
                        #return HttpResponseRedirect(reverse('conversations',kwargs={'utilisateur':user})) 
                        #return redirect('conversations',user='utilisateur')
                        return HttpResponseRedirect(reverse('discussion.views.conversations',args=[user]))
                    else:
                        return HttpResponse('Le pseudo est bon mais pas le mot de passe, essaie encore! :)')                  
            return HttpResponse('compte non existant, verifiez pseudo')

    else: # Si ce n'est pas du POST, c'est probablement une requête GET
        form = UserForm()  # Nous créons un formulaire vide
        return render(request, 'discussion/connexion.html',locals())

def conversations(request,pseudo_utilisateur):
    try:
        utilisateur=Utilisateur.objects.get(pseudo=pseudo_utilisateur)
        conversations=utilisateur.conversations.all()
        return render(request,'discussion/conversations.html',{'conversations':conversations,'utilisateur':utilisateur})
    except Utilisateur.DoesNotExist:
        return HttpResponse('Erreur')

##def creation_conversation(request,pseudo_utilisateur):
##    if request.method=='POST':
##        form=ContactForm(request.POST)
##
##        if form.is_valid():
##
##            pseudo_ami=form.cleaned_data['pseudo_ami']
##            
##            try:
##                utilisateur=Utilisateur.objects.get(pseudo=pseudo_utilisateur)
##                ami=Utilisateur.objects.get(pseudo=pseudo_ami) #on verifie si ce pseudo existe dans la base de donnée
##                envoi=true
##                nouvelle_conversation=Conversation()
##                nouvelle_conversation.paricipants.add(utilisateur,ami)
##                nouvelle_conversation.save()
##                return render(request, 'discussion/creation_conversation.html','utilisateur':utilisateur,'envoi':envoi,locals())
##            except Utilisateur.DoesNotExist:
##                return HttpResponse("""Ce pseudo n'existe pas!""")  #s'il n'existe pas -> message d'erreur              
##    else:
##        form=ContactForm()
##        return HttpResponse("Erreur, veuillez recommencer svp")
    

def accueil(request):
    return HttpResponse('Tu es bien connecté! :)')

def inscription(request):

    if request.method == 'POST':  # S'il s'agit d'une requête POST
        form = UserForm(request.POST)  # Nous reprenons les données
        
        if form.is_valid(): # Nous vérifions que les données envoyées sont valides
            
            # Ici nous pouvons traiter les données du formulaire
            pseudo = form.cleaned_data['pseudo']
            mot_de_passe = form.cleaned_data['mdp']
            user=Utilisateur(pseudo=pseudo,mot_de_passe=mot_de_passe)
            for utilisateur in Utilisateur.objects.all():
                if utilisateur.pseudo==user.pseudo:
                    return HttpResponse('Pseudo deja utilisé desolé')
            
            
            user.save()
            return redirect(accueil)

    else: # Si ce n'est pas du POST, c'est probablement une requête GET
        form = UserForm()  # Nous créons un formulaire vide
        return render(request, 'discussion/inscription.html', locals())

