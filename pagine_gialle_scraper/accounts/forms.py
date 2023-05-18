from typing import Any
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from accounts.models import UserProfile

class RegistrationUserForm(UserCreationForm):
    # email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class':'form-control'}))
    # first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    # last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
    # address = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    # phone = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = UserProfile
        fields=('username','first_name','last_name','region','phone','email','password1','password2')
    
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(RegistrationUserForm,self).__init__(*args, **kwargs) 
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Inserisci il tuo username'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Inserisci la tua password'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Inserisci la tua password'