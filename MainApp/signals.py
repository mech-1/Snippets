import logging

from django.contrib.auth.models import User  # Импортируем модель User
from django.contrib import messages
from django.db.models import F
from django.db.models.signals import post_save, pre_save, post_delete  # Импортируем post_save
from django.dispatch import receiver, Signal

from MainApp.models import Snippet, Comment, Notification

snippet_view = Signal()
logger = logging.getLogger(__name__)  # Рекомендуется использовать имя текущего модуля


# Декоратор @receiver() связывает функцию send_registration_message
# с сигналом post_save. Мы указываем, что нас интересуют только сигналы
# от модели User, и только когда created=True (т.е. пользователь был создан, а не обновлён).
# ''sender'': Аргумент ''sender'' в ''signal.send()'' и в функции-обработчике указывает, кто отправил сигнал. Это полезно, если у вас несколько разных источников, которые могут отправлять один и тот же сигнал, и вы хотите выполнить разную логику в зависимости от отправителя.
# ```'kwargs'': Используйте ''**kwargs'' в функции обработчика, чтобы получать любые дополнительные именованные аргументы, которые были переданы при отправке сигнала (например, наш user).
@receiver(post_save, sender=User)
def send_registration_message(sender, instance, created, **kwargs):
    """
    Обработчик сигнала, который выводит сообщение о регистрации пользователя в терминал.
    Срабатывает при создании нового пользователя.
    """
    if created:
        # print("New user {} created".format(instance.username))
        print(f"--- Сигнал post_save получен ---")
        print(f"Пользователь '{instance.username}' успешно зарегистрирован!")
        print(f"Отправитель: {sender.__name__}")
        print(f"ID пользователя: {instance.id}")
        print(f"--- Конец сигнала ---")


@receiver(post_save, sender=Snippet)
def send_new_snippet_message(sender, instance, created, **kwargs):
    if created:
        print('Сниппет успешно добавлен')


@receiver(snippet_view, sender=None)
def add_views_count(sender, snippet, **kwargs):
    snippet.views_count = F('views_count') + 1
    snippet.save(update_fields=["views_count"])  # -> SET v_c = 11 | SET v_c =  v_c + 1
    snippet.refresh_from_db()


@receiver(pre_save, sender=Snippet)
def check_name_length(sender, instance, **kwargs):
    # print(f"check names {instance} ")
    # print(f" length {len(instance.name)}")
    if not 3 <= len(instance.name) <= 20:
        print('name length should be between 3 and 20 characters')


@receiver(post_delete, sender=Snippet)
def log_delete_snippet(sender, instance, **kwargs):
    # print(f"snippet deleted: {instance.id} {instance.name}")
    # print(f"snippet deleted2: {instance}")
    logger.info(f"Удален сниппет: {instance.id} {instance.name}")
    # use __str__ for snippet
    logger.error(f"Удален сниппет: {instance}")


@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created and instance.snippet.user and instance.author != instance.snippet.user:
        Notification.objects.create(
            recipient=instance.snippet.user,
            comment=instance,
            notification_type='comment',
            title=f'Новый комментарий к сниппету {instance.snippet.name}',
            message=f'Пользователь "{instance.author.username}" оставил комментарий "{instance.text[:50]}{"..." if len(instance.text) > 50 else ""}"'
        )
