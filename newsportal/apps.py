from django.apps import AppConfig


class NewsportalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newsportal'

    def ready(self):
        import newsportal.signals

        # from .tasks import send_mails
        # from .scheduler import post_scheduler
        # print('started')

        # post_scheduler.add_job(

        # )
        # post_scheduler.start()