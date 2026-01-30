from django.http import HttpResponseForbidden


class OwnerRequiredMixin:
    """Только владелец записи может его редактировать"""

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != request.user:
            return HttpResponseForbidden("Не ваша запись!")
        return super().dispatch(request, *args, **kwargs)
