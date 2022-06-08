from django.db.models import fields
from user.models import DeliveryAgent
from django import forms
from .models import City, DeliveryBoy, Hub,CentralHub
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20,widget=forms.PasswordInput)

class CentralHubForm(forms.ModelForm):
    password = forms.CharField(max_length=20,widget=forms.PasswordInput)
    class Meta:
        model = CentralHub
        fields = ['state','city','username','password','email','address', 'base_fare']

class EditCentralHubForm(forms.ModelForm):
    class Meta:
        model = CentralHub
        fields = ['state','city','email','address', 'base_fare']

class HubForm(forms.ModelForm):
    password = forms.CharField(max_length=20,widget=forms.PasswordInput)
    class Meta:
        model = Hub
        fields = ['central_hub','city','username','password','email','address', 'base_fare']

class EditHubForm(forms.ModelForm):
    class Meta:
        model = Hub
        fields = ['central_hub','city','email','address', 'base_fare']

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name']

class Profile(UserChangeForm):
    username=forms.CharField(disabled=True)
    email=forms.CharField(disabled=True)
    password=forms.CharField(widget=forms.HiddenInput())
    class Meta:
        model = User
        fields = ['username', 'email']

class EditProfile(UserChangeForm):
    username=forms.CharField(disabled=True)
    password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['username', 'email']

class CityForm(forms.ModelForm):
    # state = forms.CharField(disabled=True)
    class Meta:
        model = City
        fields = ['state','city']
    
class DeliveryBoyForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = DeliveryBoy
        fields = ['hub','first_name','last_name','email', 'username','password','contact']

class DeliveryAgentForm(forms.ModelForm):
    class Meta:
        model = DeliveryAgent
        fields = ['delivery','delivery_boy']