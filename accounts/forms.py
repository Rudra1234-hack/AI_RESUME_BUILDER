from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-custom', 'placeholder': 'Password'}))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-custom', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control form-control-custom', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-custom', 'placeholder': 'Email Address'}),
        }

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match.")
        return password_confirm

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control form-control-custom'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control form-control-custom'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-custom'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'bio', 'avatar']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control form-control-custom'}),
            'bio': forms.Textarea(attrs={'class': 'form-control form-control-custom', 'rows': 4}),
            'avatar': forms.FileInput(attrs={'class': 'form-control form-control-custom'}),
        }
