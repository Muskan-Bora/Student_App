from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
import re

# class RegisterForm(UserCreationForm):
#     email = forms.EmailField()
#     first_name = forms.CharField()
#     last_name = forms.CharField()
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['username'].widget.attrs['maxlength'] = 150  # Ensure max length is correct

class RegisterForm(UserCreationForm):
    username = forms.CharField(
        max_length=30, 
        min_length=6, 
        required=True,
        help_text="Username must be between 6 to 30 characters.",
        error_messages={
            'min_length': 'Username must be at least 6 characters long.',
            'max_length': 'Username cannot exceed 30 characters.',
            'required': 'This field is required.'
        }
    )
    email = forms.EmailField(
        required=True, 
        help_text="Enter a valid email address.",
        error_messages={'invalid': 'Enter a valid email address.'}
    )
    first_name = forms.CharField(
        max_length=30, 
        required=True, 
        error_messages={'required': 'First name is required.'}
    )
    last_name = forms.CharField(
        max_length=30, 
        required=True, 
        error_messages={'required': 'Last name is required.'}
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match("^[A-Za-z0-9_]*$", username):
            raise forms.ValidationError("Username can only contain letters, numbers, and underscores.")
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose another.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match.")
        
        if len(password1) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        
        if not any(char.isdigit() for char in password1):
            raise forms.ValidationError("Password must contain at least one number.")
        
        if not any(char.isupper() for char in password1):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")

        return password2

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'roll_no', 'std', 'division', 'image']