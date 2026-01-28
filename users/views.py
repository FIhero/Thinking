from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from users.forms import CustomAuthenticationForm, CustomUserCreationForm, UserUpdateForm
from users.models import User


class RegisterUser(CreateView):
    form_class = CustomUserCreationForm
    template_name = "users/register.html"
    success_url = reverse_lazy("diary_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class LoginUser(LoginView):
    form_class = CustomAuthenticationForm
    template_name = "users/login.html"
    success_url = reverse_lazy("diary_list")


class LogoutUser(LogoutView):
    success_url = reverse_lazy("home")


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "users/profile.html"

    def get_object(self):
        return self.request.user


class UpdateProfile(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "users/profile_edit.html"

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy("profile")


class DeleteUser(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "users/profile_delete.html"
    success_url = reverse_lazy("home")

    def get_object(self):
        return self.request.user
