# coding: utf-8
from django import forms
from models import Utilisateur,Conversation,Message

def est_vide(parametre):
    length=len(parametre)
    if length==0:
            raise forms.ValidationError("Ce champs est obligatoire")
    
class InscriptionForm(forms.Form):
    
    pseudo=forms.CharField(min_length=1,max_length=20,required=False)
    telephone=forms.CharField(required=False)
    email=forms.EmailField(label="Votre adresse mail",required=False)
    mdp = forms.CharField(widget=forms.PasswordInput,min_length=1,label="mot de passe",required=False)
    

#Tout ce qui est en dessous permet de verifier qu'on envoit de bonnes données lorsqu'on s'inscrit et permet aussi d'envoyer de beaux messages d'erreurs.
    def clean_telephone(self):
        telephone = self.cleaned_data['telephone']
        est_vide(telephone)
        length = len(telephone)
        if length!=10:
            raise forms.ValidationError("Un numéro de telephone comporte 10 chiffres")
        
        try:
            premier_chiffre=telephone[0]
            verif_telephone=telephone[1:length]
            verif_telephone=int(verif_telephone)
            premier_chiffre=int(premier_chiffre)
            
        except ValueError:
             raise forms.ValidationError("Un numéro de telephone est un numero")
        if premier_chiffre!=0:
            message=str(premier_chiffre)
            raise forms.ValidationError("Un numéro de telephone commence par un 0 il me semble... ",message)
        
        for utilisateur in Utilisateur.objects.all():
            if utilisateur.telephone==telephone:
                raise forms.ValidationError("Numero deja pris, désolé")
            
        return telephone
    
    def clean_pseudo(self):
        pseudo=self.cleaned_data['pseudo']
        longueur=len(pseudo)
        est_vide(pseudo)
        
        if longueur>10:
            raise forms.ValidationError("Pas plus de 10 caractères pour un pseudo")
        for utilisateur in Utilisateur.objects.all():
            if utilisateur.pseudo==pseudo:
                raise forms.ValidationError("Pseudo deja pris, désolé")
        
        
        return pseudo
    
    def clean_mdp(self):
        mdp= self.cleaned_data['mdp']
        length=len(mdp)
        est_vide(mdp)
        return mdp
    
    def clean_email(self):
        email=self.cleaned_data['email']
        est_vide(email)
        for utilisateur in Utilisateur.objects.all():
            if utilisateur.email==email:
                raise forms.ValidationError("Adresse déja utilisée, désolé")
        return email
        
        


class ConnexionForm(forms.Form):
    identifiant=forms.CharField(max_length=20,label="inserez votre adresse mail, pseudo ou telephone svp \n",required=False)
    mdp = forms.CharField(widget=forms.PasswordInput,required=False)
    
    def clean_identifiant(self):
        identifiant=self.cleaned_data['identifiant']
        longueur=len(identifiant)
        est_vide(identifiant)
        
        return identifiant
    
    def clean_mdp(self):
        mdp= self.cleaned_data['mdp']
        est_vide(mdp)
        return mdp

class ConversationCreationForm(forms.Form):
    pseudo_ami = forms.CharField(max_length=20,required=True)
    
class ChangementForm(forms.Form):
    
    pseudo=forms.CharField(min_length=1,max_length=20,required=False)
    telephone=forms.CharField(required=False)
    email=forms.EmailField(label="Votre adresse mail",required=False)
    mdp = forms.CharField(widget=forms.PasswordInput,min_length=1,label="nouveau mot de passe",required=False)
    
    def clean_telephone(self):
        telephone = self.cleaned_data['telephone']
        est_vide(telephone)
        length = len(telephone)
        if length!=10:
            raise forms.ValidationError("Un numéro de telephone comporte 10 chiffres")
        
        try:
            premier_chiffre=telephone[0]
            verif_telephone=telephone[1:length]
            verif_telephone=int(verif_telephone)
            premier_chiffre=int(premier_chiffre)
            
        except ValueError:
             raise forms.ValidationError("Un numéro de telephone est un numero")
        if premier_chiffre!=0:
            message=str(premier_chiffre)
            raise forms.ValidationError("Un numéro de telephone commence par un 0 il me semble... ",message)
        
        try:
            utilisateur_telephone=Utilisateur.objects.get(telephone=telephone)
            return utilisateur_telephone
        except Utilisateur.DoesNotExist:
            raise forms.ValidationError("Ce numéro n'est pas présent dans la base de donnée")
            
            
    
    def clean_pseudo(self):
        pseudo=self.cleaned_data['pseudo']
        longueur=len(pseudo)
        est_vide(pseudo)
        
        if longueur>10:
            raise forms.ValidationError("Pas plus de 10 caractères pour un pseudo")
        try:
            utilisateur_pseudo=Utilisateur.objects.get(pseudo=pseudo)
            return utilisateur_pseudo
        except Utilisateur.DoesNotExist:
            raise forms.ValidationError("Ce pseudo n'est pas présent dans la base de donnée")
        
    
    def clean_mdp(self):
        mdp= self.cleaned_data['mdp']
        length=len(mdp)
        est_vide(mdp)
        return mdp
    
    def clean_email(self):
        email=self.cleaned_data['email']
        est_vide(email)
        try:
            utilisateur_email=Utilisateur.objects.get(email=email)
            return utilisateur_email
        except Utilisateur.DoesNotExist:
            raise forms.ValidationError("Cette adresse n'est pas présente dans la base de donnée")
    
