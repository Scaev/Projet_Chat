from django.db import models

class Utilisateur(models.Model):
    pseudo = models.CharField(max_length=20)
    mot_de_passe = models.CharField(max_length=20)    
#   conversations = ManyToManyField(Conversation)
    
class Message(models.Model):
	texte = models.CharField(max_length=500)
	date = date = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Date d'envoi")
	auteur = models.CharField(max_length=20)

#class Conversation(models.Model):
#	participants = ManyToManyField(Utilisateur)
#	messages = ManyToManyField(Message)
	
