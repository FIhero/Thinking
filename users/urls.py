from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.RegisterUser.as_view(), name="register"),
    path("login/", views.LoginUser.as_view(), name="login"),
    path("logout/", views.LogoutUser.as_view(), name="logout"),
    path("profile/", views.ProfileView.as_view(), name="profile"),
    path("profile/edit/", views.UpdateProfile.as_view(), name="profile_edit"),
    path("profile/delete/", views.DeleteUser.as_view(), name="profile_delete"),
]
