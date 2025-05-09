from django.views.generic import TemplateView
from .mixins import LogoutRequiredMixin

class MainView(LogoutRequiredMixin, TemplateView):
    template_name = 'main/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['welcome_message'] = 'Добро пожаловать на сайт управления умной фермой'

        return context
