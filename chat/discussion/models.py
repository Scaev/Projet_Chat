from django.db import models

class Utilisateur(models.Model):
    pseudo = models.CharField(max_length=20)
    mot_de_passe = models.CharField(max_length=20)
    telephone=models.CharField(max_length=20)
    email=models.CharField(max_length=30)

    def __str__(self):
        return self.pseudo

  
    
    
class Message(models.Model):
    texte = models.CharField(max_length=500)
    date = date = models.DateTimeField(auto_now_add=True, auto_now=False, verbose_name="Date d'envoi")
    auteur = models.ForeignKey('Utilisateur', related_name="messages")

class Conversation(models.Model):
    numero = models.CharField(max_length=20)
    participants = models.ManyToManyField(Utilisateur,related_name="conversations")
    messages = models.ManyToManyField(Message)

