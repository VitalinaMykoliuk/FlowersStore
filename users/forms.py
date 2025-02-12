from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from users.models import CustomUser


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'small mb-1', 'placeholder': 'Введите имя пользователя'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'small mb-1', 'placeholder': 'Введите адрес эл. почты'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'small mb-1', 'placeholder': 'Введите пароль'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'small mb-1', 'placeholder': 'Подтвердите пароль'})
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control py-4',
            'placeholder': 'Введите имя пользователя'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control py-4',
            'placeholder': 'Введите пароль'
        })
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'password')


class UserAccountForm(forms.ModelForm):
    profile_picture = forms.ImageField(widget=forms.FileInput(attrs={
        'class': 'custom-file-label'
    }), required=False)

    class Meta:
        model = CustomUser
        fields = ['profile_picture', 'username', 'email']
        widgets = {
            'profile_picture': forms.ClearableFileInput(attrs={'multiple': False})
        }