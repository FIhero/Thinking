from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "phone", "created_at")
    list_filter = ("is_staff", "is_superuser", "is_active")
    search_fields = ("email", "phone")
    ordering = ("-created_at",)
    list_per_page = 25
