from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from users.forms import CustomUserCreationForm
from django.contrib.auth import get_user_model

#@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', ),
        }),
    )

User = get_user_model()
admin.site.register(User, CustomUserAdmin)