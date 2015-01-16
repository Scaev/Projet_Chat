from django import forms


class UserForm(forms.Form):
    pseudo=forms.CharField(max_length=20)
    mdp = forms.CharField(widget=forms.PasswordInput)

class ConversationCreationForm(forms.Form):
    pseudo_ami = forms.CharField(max_length=20)
