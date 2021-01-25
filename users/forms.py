from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    username = forms.CharField( 
        widget=forms.TextInput( 
            attrs={'class': 'form-control'} 
        ) 
    ) 
     
    
    class Meta:
        model = User
        fields = ('username',)