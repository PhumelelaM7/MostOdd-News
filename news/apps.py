# Import Django's AppConfig
from django.apps import AppConfig


# Application configuration
class NewsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "news"

    # Import signals when the application starts
    def ready(self):
        import news.signals