# -*- coding: utf-8 -*-
from discussion.forms import UserForm
from django.http import HttpResponse
from django.shortcuts import redirect,render
from models import Utilisateur


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
                        return redirect(accueil)
                    else:
                        return HttpResponse('Le pseudo est bon mais pas le mot de passe, essaie encore! :)')
        
                
            
                    
            return HttpResponse('compte non existant, verifiez pseudo')

    else: # Si ce n'est pas du POST, c'est probablement une requête GET
        form = UserForm()  # Nous créons un formulaire vide
        return render(request, 'discussion/connexion.html',locals())


def accueil(request):
    return HttpResponse("Tu es bien connecté !:)")

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

