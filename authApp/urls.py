from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name="home"),
    path('profile/', views.user_profile_view, name='user_profile'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('protected/', views.ProtectedView.as_view(), name='protected'),
    path('api_keys/', views.api_key_view, name='api_keys'),  # Add this line
    path('search/omdb/', views.omdb_search_view, name='omdb_search'), # Add this line
    path('search/weather/', views.weather_search_view, name='weather_search'), # Add this line


]