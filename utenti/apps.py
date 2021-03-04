from django.apps import AppConfig


class UtentiConfig(AppConfig):
    name = 'utenti'
    def ready(self):
        import utenti.signals