from django.contrib import admin
from .models import UserAPIKeys
# Register your models here.

@admin.register(UserAPIKeys)
class UserAPIKeysAdmin(admin.ModelAdmin):
    list_display = ('user', 'omdb_api_key', 'weatherapi_api_key')
    search_fields = ('user__username', 'omdb_api_key', 'weatherapi_api_key')

