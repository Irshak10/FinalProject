from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = '2. Профили и доступ'

    def ready(self):
        import users.models
