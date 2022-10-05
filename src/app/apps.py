from django.apps import AppConfig as Config


class AppConfig(Config):
    name = "app"
    verbose_name = 'Отель'

default_app_config = "app.AppConfig"
