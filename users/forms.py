from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from rest_framework.exceptions import ValidationError

from .models import User


class CustomUserCreationForm(UserCreationForm):
    """Форма регистрации для кастомной модели User"""

    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ("email", "phone")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    """Форма входа по email"""

    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={
                "autofocus": True,
                "placeholder": "example@mail.com",
                "class": "form-input",
            }
        ),
    )

    def clean(self):
        email = self.cleaned_data.get("username")  # получаем email
        password = self.cleaned_data.get("password")

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise ValidationError(
                    "Пользователь с таким email не найден", code="invalid_login"
                )

            if not user.check_password(password):
                raise ValidationError("Неверный пароль", code="invalid_login")

            # Устанавливаем user_cache для Django
            self.user_cache = user

        return self.cleaned_data


class UserUpdateForm(forms.ModelForm):
    """Форма редактирования профиля"""

    class Meta:
        model = User
        fields = ("email", "phone", "avatar")
