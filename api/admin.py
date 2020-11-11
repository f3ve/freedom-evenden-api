"""
Admin site config
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from api.models import User
from django.forms import ModelForm


class ApiUserCreationForm(ModelForm):
    class Meta:
        model = User
        fields = ('email',)

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class ApiUserAdmin(UserAdmin):
    add_form = ApiUserCreationForm
    list_display = ("email",)
    ordering = ("email",)

    fieldsets = (
        (None, {'fields': ('email', 'password', 'full_name', 'username')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'username', 'full_name', 'is_superuser', 'is_staff', 'is_active')}
         ),
    )


admin.site.register(User, ApiUserAdmin)
