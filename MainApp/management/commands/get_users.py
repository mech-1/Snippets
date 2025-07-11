from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Получает список зарегистрированных пользователей"

    def add_arguments(self, parser):
        parser.add_argument(
            "--max_users",
            type=int,
            help="Ограничивает максимальное кол-во пользователей"
        )

    def handle(self, *args, **options):
        # print("Проверка принта!")
        max_users = options.get("max_users")
        users = User.objects.all()[:max_users]

        self.stdout.write("Список пользователей:")
        for user in users:
            self.stdout.write(f"{user}")
