from django.http import HttpResponseForbidden


class OwnerRequiredMixin:
    """Только владелец объекта может его редактировать"""

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != request.user:
            return HttpResponseForbidden("Не ваш объект!")
        return super().dispatch(request, *args, **kwargs)
