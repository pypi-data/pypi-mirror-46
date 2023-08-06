from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField, UserChangeForm
from django import forms

from cosmicdb.models import UserSystemMessage, UserSystemNotification


user_model = get_user_model()


class UserSystemMessageInlineAdmin(admin.TabularInline):
    model = UserSystemMessage


class UserSystemNotificationInlineAdmin(admin.TabularInline):
    model = UserSystemNotification


class CosmicDBUserCreationForm(UserCreationForm):
    class Meta:
        model = user_model
        fields = ("username", "email",)
        field_classes = {'username': UsernameField}

    def clean_email(self):
        data = self.cleaned_data['email']
        check_for_emails_qs = user_model.objects.filter(email=data).exclude(pk=self.instance.pk)
        if len(check_for_emails_qs) >= 1:
            raise forms.ValidationError("Email address is already in use.")
        return data

    def __init__(self, *args, **kwargs):
        super(CosmicDBUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True


class CosmicDBUserChangeForm(UserChangeForm):
    def clean_email(self):
        data = self.cleaned_data['email']
        check_for_emails_qs = user_model.objects.filter(email=data).exclude(pk=self.instance.pk)
        if len(check_for_emails_qs) >= 1:
            raise forms.ValidationError("Email address is already in use.")
        return data

    def __init__(self, *args, **kwargs):
        super(CosmicDBUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True


class UserProfileAdmin(UserAdmin):
    add_form = CosmicDBUserCreationForm
    form = CosmicDBUserChangeForm
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    inlines = [
        UserSystemMessageInlineAdmin,
        UserSystemNotificationInlineAdmin,
    ]


admin.site.register(user_model, UserProfileAdmin)
