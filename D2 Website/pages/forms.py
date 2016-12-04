from django import forms
from pages.models import *

class MinecraftUserForm(forms.ModelForm):
    """
    A form for editing a registered Minecraft user.
    """
    class Meta:
        model = MinecraftUser
        fields = ['username', 'password']
        labels = {
            'username': "Username",
            'password': "Password"
        }
        widgets = {
            'password': forms.TextInput(attrs={ 'type' : 'password' })
        }

class ContactForm(forms.Form):
    """
    A form which allows a user to contact the site managers.
    """
    name = forms.CharField(label="Name", max_length=50, required=False)
    email = forms.EmailField(label="Email", required=False)
    message = forms.CharField(label="Message", widget=forms.Textarea(attrs={ 'required': True }))

class SitePostForm(forms.ModelForm):
    """
    A form for editing a site post.
    """
    class Meta:
        model = SitePost
        fields = ['title', 'author', 'content']
        widgets = {
            'content': forms.Textarea()
        }