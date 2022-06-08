from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Delivery 

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20,widget=forms.PasswordInput)

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name']

class DeliveryForm(forms.ModelForm):
    user = forms.CharField(widget=forms.HiddenInput())
    type = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'e.g, Electronics, Goods, Books, Pets ...'}))
    class Meta:
        model = Delivery
        fields = ['user', 'source', 'destination', 'weight', 'type', 'destination_person', 'destination_address', 'destination_contact']