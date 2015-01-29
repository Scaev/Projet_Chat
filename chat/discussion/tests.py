# coding: utf-8
from django.test import TestCase
from discussion.views import *
from models import Utilisateur,Conversation,Message

from random import randint

import random, string

def randomword(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))

def Numero_aleatoire():
    entier_aleatoire=randint(0,999999999);
    entier_aleatoire=str(entier_aleatoire);
    # il faut ici rajouter les 0
    nombre_zero_a_rajouter=10-len(entier_aleatoire);
    numero=nombre_zero_a_rajouter*'0'+entier_aleatoire;
    return numero

class InscriptionTests(TestCase):
    def test_est_rempli(self):
        """
       On va verifier si lorsqu'un utilisateur donne des parametres faux, le formulaire est effectivement renvoyé
       """
        form_data = {'pseudo': 'test','telephone':'0000000000','email':'test@test.fr','mdp':''}
        form = InscriptionForm(data=form_data)
        self.assertEqual(form.is_valid(), False) # formulaire sans mdp 
        
        form_data = {'pseudo': 'test','telephone':'0000000000','email':'','mdp':'test'}
        form = InscriptionForm(data=form_data)
        self.assertEqual(form.is_valid(), False) # formulaire sans mail
        
        form_data = {'pseudo': 'test','telephone':'','email':'test@test.fr','mdp':'test'}
        form = InscriptionForm(data=form_data)
        self.assertEqual(form.is_valid(), False) # formulaire sans telephone 
        
        form_data = {'pseudo': '','telephone':'0000000000','email':'test@test.fr','mdp':'test'}
        form = InscriptionForm(data=form_data)
        self.assertEqual(form.is_valid(), False) # sans pseudo 

    def test_est_numero(self):

        form_data = {'pseudo': 'test','telephone':'qjod6320ds','email':'test@test.fr','mdp':'test'}
        form = InscriptionForm(data=form_data)
        self.assertEqual(form.is_valid(), False) # numero non integralement rempli de chiffre

        form_data = {'pseudo': 'test','telephone':'012345678','email':'test@test.fr','mdp':'test'}
        form = InscriptionForm(data=form_data)
        self.assertEqual(form.is_valid(), False) # numero qui n' a pas 10 chiffres
        
        form_data = {'pseudo': 'test','telephone':'9876543210','email':'test@test.fr','mdp':'test'}
        form = InscriptionForm(data=form_data)
        self.assertEqual(form.is_valid(), False) # numero qui ne commence pas par 0 

        numero=Numero_aleatoire()
        form_data = {'pseudo': 'test','telephone':numero,'email':'test@test.fr','mdp':'test'}
        form = InscriptionForm(data=form_data)
        self.assertEqual(form.is_valid(), True) # si le numéro a la bonne forme 
        
    def test_est_email(self):
        
        form_data = {'pseudo': 'test','telephone':'0876543210','email':'testtest.fr','mdp':'test'}
        form = InscriptionForm(data=form_data)
        self.assertEqual(form.is_valid(), False) # pas de @ 

        form_data = {'pseudo': 'test','telephone':'0876543210','email':'test@@test.fr','mdp':'test'}
        form = InscriptionForm(data=form_data)
        self.assertEqual(form.is_valid(), False) # 2 @

        

        email_test=randomword(6)+'@'+randomword(4)+'.'+randomword(2)
        form_data = {'pseudo': 'test','telephone':'0876543210','email':email_test,'mdp':'test'}
        form = InscriptionForm(data=form_data)
        self.assertEqual(form.is_valid(), True)

    def test_identifiant_libre(self):
        
        pseudo_test=randomword(7)
        mot_de_passe_test=randomword(5)
        numero=Numero_aleatoire()
        email_test=randomword(6)+'@'+randomword(4)+'.'+randomword(2)
        
        user=Utilisateur(pseudo=pseudo_test,mot_de_passe=mot_de_passe_test,telephone=numero,email=email_test)
        user.save()

        form_data = {'pseudo': pseudo_test,'telephone':'0123456789','email':'test@test.fr','mdp':'test'}
        form = InscriptionForm(data=form_data)
        self.assertEqual(form.is_valid(), False) # si le pseudo est deja occupé

        form_data = {'pseudo': 'test','telephone':numero,'email':'test@test.fr','mdp':'test'}
        form = InscriptionForm(data=form_data)
        self.assertEqual(form.is_valid(), False) # si le telephone est occupé

        form_data = {'pseudo': 'test','telephone':'0123456789','email':email_test,'mdp':'test'}
        form = InscriptionForm(data=form_data)
        self.assertEqual(form.is_valid(), False) # si le pseudo est deja occupé
        
class ConversationsTest(TestCase):
    def test_est_vide(self):
        