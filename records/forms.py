from django import forms

from .models import Diary


class DiaryCreateForm(forms.ModelForm):
    """Форма создания записи дневника"""

    class Meta:
        model = Diary
        fields = ("title", "text", "mood", "date", "image_file", "music_link")
        widgets = {
            "text": forms.Textarea(
                attrs={"rows": 5, "placeholder": "Что интересного было сегодня?"}
            ),
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "mood": forms.Select(choices=Diary.mood_choices),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["date"].required = False


class DiaryUpdateForm(forms.ModelForm):
    """Форма редактирования записи"""

    class Meta:
        model = Diary
        fields = ("title", "text", "mood", "date", "image_file", "music_link")
