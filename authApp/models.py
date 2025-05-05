# authApp/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator

class UserAPIKeys(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='api_keys')
    omdb_api_key = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)]) # Store max 100 character API keys. Adjust max_length as necessary.
    weatherapi_api_key = models.CharField(max_length=100, blank=True, null=True, validators=[MaxLengthValidator(100)])
    # Add other service keys as needed

    def __str__(self) -> str:
        return f"API Keys for {self.user.username if self.user else 'Unknown User'}"


