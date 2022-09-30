from dataclasses import field
from pyexpat import model
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Lavadero, SolicitudLavadero, Tarifa

# Aca abajo creamos los forms

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            
        return user

class NewLavaderoForm(forms.ModelForm):
    class Meta:
        model = Lavadero
        fields = ['nombre', 'direccion', 'telefono', 'telefono_aux', 'encargado', 'imagen']

class NewTarifaForm(forms.ModelForm):
    class Meta:
        model = Tarifa
        fields = ['tipo', 'monto']

class NewSolicitarLavado(forms.ModelForm):
    class Meta:
        model = SolicitudLavadero
        fields = ['tipo']



