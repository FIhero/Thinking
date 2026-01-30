from django.core.validators import URLValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone

from users.models import User


class Diary(models.Model):
    """Модель личного дневника"""

    mood_choices = [
        (1, "🙂 Хорошо"),
        (2, "😀 Отлично"),
        (3, "🥰 Влюблён"),
        (4, "😡 Злой"),
        (5, "😐 Нормально"),
        (6, "🤔 Задумчивый"),
        (7, "😢 Грустный"),
        (8, "😭 Плачу"),
    ]
    mood = models.IntegerField(
        choices=mood_choices, default=5, verbose_name="Настроение"
    )

    title = models.CharField(
        verbose_name="Заголовок",
        max_length=255,
    )
    text = models.TextField(
        help_text="Что интересного было сегодня?",
        blank=True,
    )
    date = models.DateField(
        verbose_name="Дата записи",
        default=timezone.now,
    )

    image_file = models.ImageField(
        upload_to="diary_images/%Y/%m/%d/",
        verbose_name="Изображение",
        help_text="Изображение для записи",
        blank=True,
        null=True,
    )
    music_link = models.URLField(
        blank=True,
        verbose_name="Ссылка на музыку",
        help_text="Ссылка на YouTube, Spotify, Яндекс.Музыку, VK музыка",
        validators=[URLValidator()],
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        related_name="diaries",
    )

    class Meta:
        verbose_name = "Запись личного дневника"
        verbose_name_plural = "Записи личного дневника"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.owner.email})"

    def get_absolute_url(self):
        return reverse("diary_detail", kwargs={"pk": self.pk})

    def get_mood_emoji(self):
        return dict(self.mood_choices).get(self.mood, "").split()[0]

    def get_mood_text(self):
        value = dict(self.mood_choices).get(self.mood, "")
        return value.split(" ", 1)[1] if " " in value else value
