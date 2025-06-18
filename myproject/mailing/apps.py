from django.apps import AppConfig


class MailingAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mailing"

    def ready(self):
        from .service import start_scheduler

        start_scheduler()
