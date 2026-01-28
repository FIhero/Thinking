from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email обязателен")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField("Email", max_length=254, unique=True)
    phone = models.CharField("Телефон", max_length=20, blank=True, default="")
    avatar = models.ImageField(
        upload_to="users/",
        blank=True,
        null=True,
        default="users/default_user.png",
        verbose_name="Аватар",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    groups = models.ManyToManyField(
        "auth.Group",
        verbose_name="Группы",
        blank=True,
        related_name="custom_user_set",
        help_text="Группы, к которым принадлежит пользователь",
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name="Права пользователя",
        blank=True,
        related_name="custom_user_permissions_set",
        help_text="Права этого пользователя",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
