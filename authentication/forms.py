
from django import forms
from django.contrib.auth.forms import UserCreationForm
from authentication.models import User


class UserRegisterForm(UserCreationForm):
    password1: forms.CharField(label='Contraseña',widget=forms.PasswordInput)
    password2: forms.CharField(label='Confirmar Contraseña',widget=forms.PasswordInput)
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
    class Meta:
        model = User
        fields = ['username','email','password1','password2']