from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('username', 'email')
    empty_value_display = '-пусто-'
