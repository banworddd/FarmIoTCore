from django import forms
from .models import CustomUser
import re

class CustomUserRegistrationForm(forms.ModelForm):
    """
    Форма регистрации пользователя.

    Атрибуты:
        password (CharField): Поле для ввода пароля.
        password2 (CharField): Поле для подтверждения пароля.
        phone_number (CharField): Поле для ввода номера телефона.
    """

    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput,
        help_text="Пароль должен содержать минимум 8 символов, цифры и буквы в разных регистрах"
    )
    password2 = forms.CharField(
        label='Подтвердите пароль',
        widget=forms.PasswordInput
    )
    phone_number = forms.CharField(
        label='Номер телефона',
        widget=forms.TextInput(attrs={
            'class': 'phone-input',
            'placeholder': '+7 (XXX) XXX-XX-XX'
        }),
        max_length=18
    )

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'phone_number', 'email', 'password')
        labels = {
            'phone_number': 'Номер телефона',
            'email': 'Email (необязательно)'
        }
        help_texts = {
            'phone_number': 'Формат: 9876543210 (10 цифр)',
        }

    def clean_phone_number(self):
        """
        Валидация номера телефона.

        Возвращает:
            str: Очищенный номер телефона.

        Исключения:
            ValidationError: Если номер телефона некорректен или уже существует.
        """
        phone_number = self.cleaned_data.get('phone_number')

        if not phone_number:
            raise forms.ValidationError('Номер телефона обязателен')

        cleaned_phone = re.sub(r'\D', '', phone_number)

        if len(cleaned_phone) != 10:
            raise forms.ValidationError('Номер телефона должен содержать 10 цифр')

        if CustomUser.objects.filter(phone_number=cleaned_phone).exists():
            raise forms.ValidationError('Пользователь с таким номером телефона уже существует')

        return cleaned_phone

    def clean_password(self):
        """
        Валидация пароля.

        Возвращает:
            str: Пароль, если он прошел все проверки.

        Исключения:
            ValidationError: Если пароль не соответствует требованиям.
        """
        password = self.cleaned_data.get('password')

        if len(password) < 8:
            raise forms.ValidationError('Пароль должен содержать минимум 8 символов')

        if not any(char.isdigit() for char in password):
            raise forms.ValidationError('Пароль должен содержать хотя бы одну цифру')

        if not any(char.isupper() for char in password):
            raise forms.ValidationError('Пароль должен содержать хотя бы одну заглавную букву')

        if not any(char.islower() for char in password):
            raise forms.ValidationError('Пароль должен содержать хотя бы одну строчную букву')

        return password

    def clean_email(self):
        """
        Валидация email.

        Возвращает:
            str: Email, если он уникален.

        Исключения:
            ValidationError: Если email уже существует.
        """
        email = self.cleaned_data.get('email')
        if email and CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует')
        return email

    def clean_first_name(self):
        """
        Валидация имени.

        Возвращает:
            str: Имя, если оно содержит только буквы.

        Исключения:
            ValidationError: Если имя содержит недопустимые символы.
        """
        first_name = self.cleaned_data.get('first_name')
        if not first_name.isalpha():
            raise forms.ValidationError('Имя может содержать только буквы')
        return first_name

    def clean_last_name(self):
        """
        Валидация фамилии.

        Возвращает:
            str: Фамилия, если она содержит только буквы.

        Исключения:
            ValidationError: Если фамилия содержит недопустимые символы.
        """
        last_name = self.cleaned_data.get('last_name')
        if not last_name.isalpha():
            raise forms.ValidationError('Фамилия может содержать только буквы')
        return last_name

    def clean(self):
        """
        Валидация соответствия паролей.

        Возвращает:
            dict: Очищенные данные.

        Исключения:
            ValidationError: Если пароли не совпадают.
        """
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password and password2 and password != password2:
            raise forms.ValidationError('Пароли не совпадают')

        return cleaned_data

    def save(self, commit=True):
        """
        Сохранение пользователя с хешированным паролем.

        Аргументы:
            commit (bool): Флаг для сохранения пользователя в базе данных.

        Возвращает:
            CustomUser: Сохраненный пользователь.
        """
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class CustomUserConfirmationForm(forms.Form):
    """
    Форма подтверждения регистрации пользователя.

    Атрибуты:
        confirmation_code (CharField): Поле для ввода кода подтверждения.
    """

    confirmation_code = forms.CharField(
        label='Код подтверждения',
        widget=forms.TextInput(attrs={'autocomplete': 'off'})
    )

    def __init__(self, *args, **kwargs):
        """
        Инициализация формы с добавлением объекта запроса.

        Аргументы:
            *args: Позиционные аргументы.
            **kwargs: Именованные аргументы.
        """
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        """
        Валидация кода подтверждения.

        Возвращает:
            dict: Очищенные данные.

        Исключения:
            ValidationError: Если код подтверждения неверен или сессия истекла.
        """
        cleaned_data = super().clean()
        user_input_code = cleaned_data.get('confirmation_code')

        session_code = self.request.session.get('confirmation_code')

        if not session_code:
            raise forms.ValidationError('Сессия истекла, запросите код повторно')

        if session_code != user_input_code:
            raise forms.ValidationError('Неверный код подтверждения')

        return cleaned_data
