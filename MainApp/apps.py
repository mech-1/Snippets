from django.apps import AppConfig


class MainappConfig(AppConfig):
    name = 'MainApp'

    def ready(self):
        # Импортируем sender, чтобы зарегистрировать их.
        import MainApp.signals