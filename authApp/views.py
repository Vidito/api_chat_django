# To handle views and redirects
from django.shortcuts import render, redirect
# To Import auth functions form Django
from django.contrib.auth import authenticate, login, logout
# The login_required decorator to protect views
from django.contrib.auth.decorators import login_required
# For class-based views[CBV]
from django.contrib.auth.mixins import LoginRequiredMixin
# For class-based views[CBV]
from django.views import View
#  Import the User class (model)
from django.contrib.auth.models import User
# Import the RegisterForm from forms.py
from .forms import RegisterForm
from .models import UserAPIKeys
from django.contrib import messages
from .forms import APIKeyForm, OMDBSearchForm # Import the new form
import requests


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form':form})


def login_view(request):
    error_message = None 
    if request.method == "POST":  
        username = request.POST.get("username")  
        password = request.POST.get("password")  
        user = authenticate(request, username=username, password=password)  
        if user is not None:  
            login(request, user)  
            next_url = request.POST.get('next') or request.GET.get('next') or 'home'  
            return redirect(next_url) 
        else:
            error_message = "Invalid credentials"  
    return render(request, 'accounts/login.html', {'error': error_message})

    
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')
    else:
        return redirect('home')

# Home View
# Using the decorator 
@login_required
def home_view(request):
    return render(request, 'auth1_app/home.html')

# Protected View 
class ProtectedView(LoginRequiredMixin, View):
    login_url = '/login/'
    # 'next' - to redirect URL
    redirect_field_name = 'redirect_to'
    
    def get(self, request):
        return render(request, 'registration/protected.html')


@login_required
def api_key_view(request):
    try:
        user_api_keys = request.user.api_keys
    except UserAPIKeys.DoesNotExist:
         user_api_keys = UserAPIKeys(user=request.user)

    if request.method == 'POST':
        form = APIKeyForm(request.POST, instance=user_api_keys)
        if form.is_valid():
            form.save()
            messages.success(request, 'API keys saved successfully!')
            return redirect('home')  # Or wherever you want to redirect
        else:
             messages.error(request, 'There was an error saving your API keys.  Please check the form.')
    else:
        form = APIKeyForm(instance=user_api_keys)

    return render(request, 'authApp/api_key.html', {'form': form})


@login_required
def omdb_search_view(request):
    form = OMDBSearchForm()
    results = None
    error_message = None
    omdb_key = None

    if request.method == 'POST':
        form = OMDBSearchForm(request.POST)
        if form.is_valid():
            search_term = form.cleaned_data['search_term']

            try:
                # Retrieve the user's OMDB API key
                user_api_keys = request.user.api_keys
                omdb_key = user_api_keys.omdb_api_key

                if not omdb_key:
                    error_message = "You have not saved an OMDB API key yet. Please add it on the API Keys page."
                else:
                    # Make the API call to OMDB
                    omdb_url = f"https://www.omdbapi.com/?s={search_term}&apikey={omdb_key}"
                    response = requests.get(omdb_url)
                    response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
                    data = response.json()

                    if data.get('Response') == 'True':
                        results = data.get('Search')
                    else:
                        error_message = data.get('Error', 'An unknown error occurred with the OMDB API.')

            except UserAPIKeys.DoesNotExist:
                error_message = "Please save your API keys on the API Keys page."
            except requests.exceptions.RequestException as e:
                error_message = f"Error connecting to OMDB API: {e}"
            except Exception as e:
                error_message = f"An unexpected error occurred: {e}"

    return render(request, 'authApp/omdb_search.html', {
        'form': form,
        'results': results,
        'error_message': error_message
    })


@login_required
def user_profile_view(request):
    """
    Displays the logged-in user's profile information and API keys.
    """
    user = request.user
    user_api_keys = None
    try:
        user_api_keys = user.api_keys
    except UserAPIKeys.DoesNotExist:
        # Handle the case where the user doesn't have an associated UserAPIKeys object yet
        pass # user_api_keys remains None

    context = {
        'user': user,
        'user_api_keys': user_api_keys,
    }
    return render(request, 'authApp/user_profile.html', context)