from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from .models import Answer, Question, User

UserModel = get_user_model()

class Login_form(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'auth__input', 'placeholder': ' '}), required=True,  label="")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'auth__input', 'placeholder': ' '}), required=True, label="")    


class Register_form(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'auth__input', 'placeholder': ' ', 'autocomplete': 'off'}), max_length=16, label="")
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'auth__input', 'placeholder': ' ', 'maxlenght': "50", 'autocomplete': 'off'}), label="")
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'auth__input',  'placeholder': ' ', 'maxlenght': "50", 'autocomplete': 'off'}), label="")
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'auth__input', 'placeholder': ' ', 'autocomplete': 'off'}), label="")
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'auth__input', 'placeholder': ' ', 'autocomplete': 'off'}), label="")
    confirmation = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'auth__input', 'placeholder': ' ', 'autocomplete': 'off'}), label="")    
    
    def clean_username(self):
        ''' verify is the username is already taken.'''
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(_("Username already taken"), code="username taken")
        return username
    
    def clean_email(self):
        ''' verify if the email is already registered '''
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("Email has already been taken."), code="email taken")

        return email

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'].lower(),
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'].lower(),
            password=self.cleaned_data['password']
        )
        user.save()
        return user


class SettingsForm(forms.ModelForm):
    class Meta:
       model = User
       fields = ["username", "first_name", "last_name", "email"]

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form__input', 'id': 'username', 'placeholder': ' ', 'autocomplete': 'off'}), max_length=16, label="")
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form__input', 'id': 'first_name', 'placeholder': ' ', 'maxlenght': "50", 'autocomplete': 'off'}), label="")
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form__input', 'id': 'last_name',  'placeholder': ' ', 'maxlenght': "50", 'autocomplete': 'off'}), label="")
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form__input', 'id': 'email', 'placeholder': ' ', 'autocomplete': 'off'}), label="")

    def clean_username(self):
        ''' verify is the username is already taken.'''
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(_("Username already taken"), code="username taken")
        return username
    
    def clean_email(self):
        ''' verify if the email is already registered '''
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("Email has already been taken."), code="email taken")

        return email


class Change_password_form(forms.Form):

    error_messages = {
        'password_incorrect': _("Your old password was entered incorrectly. Please enter it again."),
        'password_mismatch': _('passwords must match'),
    }

    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form__input', 'placeholder': _('old password')}), required=True, label="")
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form__input', 'placeholder': _('password')}), required=True, label="")
    new_password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form__input', 'placeholder': _('password confirmation')}), required=True, label="")

    def clean_old_password(self):
        """
        Validate that the old_password field is correct.
        """

        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password