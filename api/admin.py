"""
Admin site config
"""

from django.forms import ModelForm
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from api.models import User


class ApiUserCreationForm(ModelForm):
    """
    custom user creation form that properly encrypts passwords
    """
    class Meta:
        model = User
        fields = ('email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class ApiUserAdmin(UserAdmin):
    """
    Defining fields that will be in the user detail page
    """
    add_form = ApiUserCreationForm
    list_display = ("username",)
    ordering = ("username",)

    fieldsets = (
        (None, {'fields': ('email', 'password', 'full_name', 'username')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password', 'username', 'full_name', 'is_superuser',
                'is_staff', 'is_active'
            )
        }),
    )


admin.site.register(User, ApiUserAdmin)
