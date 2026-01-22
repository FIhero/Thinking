from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from records.forms import DiaryCreateForm, DiaryUpdateForm
from records.mixins import OwnerRequiredMixin
from records.models import Diary


class HomeView(TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Главная страница"
        return context


class DiaryCreateView(LoginRequiredMixin, CreateView):
    model = Diary
    form_class = DiaryCreateForm
    template_name = "records/diary_create.html"
    success_url = reverse_lazy("diary_detail")

    def form_valid(self, form):
        """Устанавливаем владельца"""
        form.instance.owner = self.request.user
        return super().form_valid(form)


class DiaryUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Diary
    form_class = DiaryUpdateForm
    template_name = "records/diary_create.html"
    success_url = reverse_lazy("diary_detail")


class DiaryDetailView(LoginRequiredMixin, OwnerRequiredMixin, DetailView):
    model = Diary
    template_name = "records/dairy_detail.html"


class DiaryListView(LoginRequiredMixin, ListView):
    model = Diary
    template_name = "records/diary_list.html"
    paginate_by = 20

    def get_queryset(self):
        """Только записи текущего пользователя, отсортированные по дате
        и поиск по заголовку, дате, настроению"""
        queryset = Diary.objects.filter(owner=self.request.user)

        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(title__icontains=search)

        mood = self.request.GET.get("mood")
        if mood:
            queryset = queryset.filter(mood=mood)

        return queryset.order_by("-created_at")

    def get_context_data(self, **kwargs):
        """Дополнительные данные в контекст"""
        context = super().get_context_data(**kwargs)
        context["total_count"] = self.get_queryset().count()
        return context


class DiaryDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Diary
    template_name = "records/diary_delete.html"
    success_url = reverse_lazy("diary_list")
