from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models_auth import CustomUser

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    phone = forms.CharField(required=False, label='Телефон')
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone', 'role', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].widget.attrs.update({'class': 'form-select'})

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя или Email')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Введите имя пользователя или email'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Введите пароль'})