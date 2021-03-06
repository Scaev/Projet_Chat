# coding: utf-8
from django import forms
from models import Utilisateur,Conversation,Message
import hashlib

def est_vide(parametre):
    length=len(parametre)
    if length==0:
            raise forms.ValidationError("Ce champs est obligatoire")
    
class InscriptionForm(forms.Form):
    
    pseudo=forms.CharField(min_length=1,max_length=20,required=False)
    telephone=forms.CharField(required=False)
    email=forms.EmailField(label="Mail",required=False)
    mdp = forms.CharField(widget=forms.PasswordInput,min_length=1,label="Mot de passe",required=False)
    

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
    identifiant=forms.CharField(max_length=20,label="Pseudo, mail ou telephone",required=False)
    mdp = forms.CharField(widget=forms.PasswordInput,required=False)
    
    def clean_identifiant(self):
        existant=False
        identifiant=self.cleaned_data['identifiant']
        est_vide(identifiant)
        
        for utilisateur in Utilisateur.objects.all():
            if identifiant==utilisateur.pseudo or identifiant==utilisateur.telephone or identifiant==utilisateur.email:
                existant=True
        
                
        if existant==False:
            raise forms.ValidationError("Compte non identifié, verifiez paramètres.")
        
        
        return identifiant
    
    def clean_mdp(self):
        mdp= self.cleaned_data['mdp']
        est_vide(mdp)
        
        return mdp
    def clean(self):
        cleaned_data = super(ConnexionForm, self).clean()
        mdp= cleaned_data.get('mdp')
        identifiant=cleaned_data.get('identifiant')
        if mdp and identifiant:
            for utilisateur in Utilisateur.objects.all():
                if identifiant==utilisateur.pseudo or identifiant==utilisateur.telephone or identifiant==utilisateur.email:
                    compte=utilisateur
            mdp_hash = hashlib.md5()
	    mdp = "cHa473s" + mdp + "40b1";
            mdp_hash.update(mdp)
            if compte.mot_de_passe!=mdp_hash.hexdigest():
                self.add_error('mdp', "Le mot de passe est erroné")

        return cleaned_data
            







class ConversationCreationForm(forms.Form):
    pseudo_ami = forms.CharField(max_length=20,required=False)
    
    def clean_pseudo(self):
        existant=False
        pseudo_ami=self.cleaned_data['pseudo_ami']
        est_vide(pseudo_ami)
        


        return pseudo_ami


class ChangementForm(forms.Form):
    
    pseudo=forms.CharField(min_length=1,max_length=20,required=False)
    telephone=forms.CharField(required=False)
    email=forms.CharField(label="Votre adresse mail",required=False)
    mdp = forms.CharField(widget=forms.PasswordInput,min_length=1,label="Nouveau mot de passe",required=False)
    
      

    def clean(self):
        cleaned_data = super(ChangementForm, self).clean()
        email= cleaned_data.get('email')
        pseudo=cleaned_data.get('pseudo')
        telephone=cleaned_data.get('telephone')
        mdp=cleaned_data.get('mdp')
        valide=True
        if len(email)==0:
            self.add_error('email', "Ce champs est obligatoire")
            valide=False
        if len(pseudo)==0:
            self.add_error('pseudo', "Ce champs est obligatoire")
            valide=False
        if len(telephone)==0:
            self.add_error('telephone', "Ce champs est obligatoire")
            valide=False
        if len(mdp)==0:
            self.add_error('mdp', "Ce champs est obligatoire")
            valide=False
        if valide:    
            try:
                utilisateur_pseudo=Utilisateur.objects.get(pseudo=pseudo).pseudo
            except Utilisateur.DoesNotExist:
                self.add_error('pseudo', "Pseudo non existant")
                valide=False
       
            try:
                utilisateur_email=Utilisateur.objects.get(email=email).pseudo
            except Utilisateur.DoesNotExist:
                self.add_error('email', "Adresse non présente dans la base")
                valide=False
        
            try:  
                utilisateur_telephone=Utilisateur.objects.get(telephone=telephone).pseudo
            except Utilisateur.DoesNotExist:
                self.add_error('telephone', "Telephone non présent dans la base")
                valide=False
        
            
        if valide:
            if utilisateur_pseudo== utilisateur_telephone and utilisateur_pseudo==utilisateur_email:
                pass
            else:
                self.add_error('pseudo', "Vos données ne concordent pas")
        return cleaned_data


class EnvoiMessage(forms.Form):
    texte=forms.CharField(max_length=500,widget=forms.Textarea, label="")


class AjoutAmiForm(forms.Form):
    pseudo_ami = forms.CharField(min_length=1,max_length=20,required=False,label="Pseudo ami")
    
    def clean_pseudo_ami(self):
        existant=False
        identifiant=self.cleaned_data['pseudo_ami']
        est_vide(identifiant)
        
        for utilisateur in Utilisateur.objects.all():
            if identifiant==utilisateur.pseudo:
                existant=True        
        if existant==False:
            raise forms.ValidationError("Compte non identifié, verifiez paramètres.")
        return identifiant    

