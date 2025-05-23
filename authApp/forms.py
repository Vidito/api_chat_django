from django import forms
from django.contrib.auth.models import User
from .models import UserAPIKeys
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'appearance-none block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm placeholder-gray-400 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm'
        })
    )

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields  = ['username', 'password', 'password_confirm']
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        # Check if the passwords match
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match!")
        return cleaned_data
        

class APIKeyForm(forms.ModelForm):
    class Meta:
        model = UserAPIKeys
        fields = ['omdb_api_key', 'weatherapi_api_key'] # Add other service keys here

        widgets = {
            'omdb_api_key': forms.TextInput(attrs={'class': 'form-control'}),
            'weatherapi_api_key': forms.TextInput(attrs={'class': 'form-control'}),
        }




# Add a search form
class OMDBSearchForm(forms.Form):
    search_term = forms.CharField(label='Search Movie Title', max_length=100, required=True)

class WeatherSearchForm(forms.Form):
    search_term = forms.CharField(label='Enter city name', max_length=100, required=True)