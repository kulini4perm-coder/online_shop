from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserCreateForm(UserCreationForm):
    phone = forms.CharField(max_length=20, required=False, help_text='Необязательное поле. Введите номер телефона')
    country = forms.CharField(max_length=100, required=False, help_text='Необязательное поле. Введите страну')
    avatar = forms.ImageField(required=False, help_text='Необязательное поле. Загрузите аватар')
    username = forms.CharField(max_length=50, required=True)
    usable_password = None

    class Meta:
        model = User
        fields = ['email', 'username', 'first_name', 'last_name', 'phone', 'country', 'avatar']

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            clean_digits = phone.replace('+', '').replace(' ', '').replace('-', '')
            if not clean_digits.isdigit():
                raise forms.ValidationError('Номер должен состоять только из цифр')
        return phone
