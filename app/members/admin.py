from django.contrib import admin

# from .models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class UserAdmin(admin.ModelAdmin):
    list_display = ['username']


admin.site.register(User, UserAdmin)
