from django import forms
from cart.models import Order


class OrderCreateForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Ivan'
    }))

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'ivanivanov@gmail.com'
    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Kyiv, Berkovetskaz, 45'
    }))

    message = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control', 'placeholder': 'Enter your message here'
    }))

    class Meta:
        model = Order
        fields = ('name', 'email', 'address', 'message')