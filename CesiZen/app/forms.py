from django import forms
from django.contrib.auth.models import *
from .models import *

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password',]
        widgets = {
            'password': forms.PasswordInput(),
        }

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name',]


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['title', 'description', 'image', 'video_url', 'category', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class InformationForm(forms.ModelForm):
    class Meta:
        model = Information
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded p-2 focus:ring-indigo-500 focus:border-indigo-500'
            }),
        }