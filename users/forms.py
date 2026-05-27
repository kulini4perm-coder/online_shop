from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class UserCreateForm(UserCreationForm):
    phone_number = forms.CharField(max_length=20, required=False, help_text='Необязательное поле. Введите номер телефона')
    country = forms.CharField(max_length=100, required=False, help_text='Необязательное поле. Введите страну')
    avatar = forms.ImageField(required=False, help_text='Необязательное поле. Загрузите аватар')
    username = forms.CharField(max_length=50, required=True)
    usable_password = None

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'country', 'avatar']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number:
            clean_digits = phone_number.replace('+', '').replace(' ', '').replace('-', '')
            if not clean_digits.isdigit():
                raise forms.ValidationError('Номер должен состоять только из цифр')
        return phone_number


# Редактирование профиля
class UserProfileForm(UserChangeForm):
    password = None

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'country', 'avatar']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})