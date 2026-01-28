from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
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

    def get_success_url(self):
        return reverse("diary_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        """Устанавливаем владельца"""
        form.instance.owner = self.request.user
        return super().form_valid(form)


class DiaryUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Diary
    form_class = DiaryUpdateForm
    template_name = "records/diary_update.html"


class DiaryDetailView(LoginRequiredMixin, OwnerRequiredMixin, DetailView):
    model = Diary
    template_name = "records/diary_detail.html"


class DiaryListView(LoginRequiredMixin, ListView):
    model = Diary
    template_name = "records/diary_list.html"
    paginate_by = 20
    context_object_name = "entries"

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


# Будущее за горами


class IdeasDemoView(TemplateView):
    template_name = "ideas_demo.html"


class HealthDemoView(TemplateView):
    template_name = "health_demo.html"


class FinanceDemoView(TemplateView):
    template_name = "finance_demo.html"
