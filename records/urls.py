from django.urls import path

from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("list/", views.DiaryListView.as_view(), name="diary_list"),
    path("create/", views.DiaryCreateView.as_view(), name="diary_create"),
    path("<int:pk>/", views.DiaryDetailView.as_view(), name="diary_detail"),
    path("<int:pk>/update/", views.DiaryUpdateView.as_view(), name="diary_update"),
    path("<int:pk>/delete/", views.DiaryDeleteView.as_view(), name="diary_delete"),
    path("ideas/", views.IdeasDemoView.as_view(), name="ideas_demo"),
    path("health/", views.HealthDemoView.as_view(), name="health_demo"),
    path("finance/", views.FinanceDemoView.as_view(), name="finance_demo"),
]
