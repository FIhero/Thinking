from django.contrib import admin

from records.models import Diary


@admin.register(Diary)
class DiaryAdmin(admin.ModelAdmin):
    list_display = ["title", "date", "owner", "has_image", "created_at", "updated_at"]
    list_filter = ["created_at", "owner", "title"]
    search_fields = ["title", "text", "owner__email"]
    ordering = ["-created_at"]
    list_per_page = 50

    def has_image(self, obj):
        return bool(obj.image)

    has_image.short_description = "Есть фото"
    has_image.boolean = True

    def save_model(self, request, obj, form, change):
        if not change:
            obj.owner = request.user
        super().save_model(request, obj, form, change)
