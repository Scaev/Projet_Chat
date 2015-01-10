from django import forms


class UserForm(forms.Form):
    pseudo=forms.CharField(max_length=10)
    mdp = forms.CharField(widget=forms.PasswordInput)
