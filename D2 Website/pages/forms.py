from django import forms
from pages.models import MinecraftUser

class MinecraftUserForm(forms.ModelForm):
    """
    A form for editing a registered Minecraft user.
    """
    class Meta:
        model = MinecraftUser
        fields = ['username', 'password']
        labels = {
            'username': "Username",
        }

class ContactForm(forms.Form):
    """
    A form which allows a user to contact the site managers.
    """
    name = forms.CharField(label="Name", max_length=50, required=False)
    email = forms.EmailField(label="Email", required=False)
    message = forms.CharField(label="Message", widget=forms.Textarea)