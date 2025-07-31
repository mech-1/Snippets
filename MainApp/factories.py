import factory
from django.contrib.auth.models import User
from .models import Snippet, Comment, Tag


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User  # Указываем, какую модель будет создавать эта фабрика
        django_get_or_create = ('username',)  # Опционально: предотвращает создание дубликатов по username
        skip_postgeneration_save = True

    username = factory.Sequence(lambda n: f'user_{n}')  # Генерирует user_0, user_1 и т.д.
    email = factory.LazyAttribute(lambda o: f'{o.username}@example.com')  # Зависит от других полей
    password = factory.PostGenerationMethodCall('set_password', 'defaultpassword')  # Для хеширования пароля

    @factory.post_generation
    def save_password_changes(self, create, extracted, **kwargs):
        if create:
            self.save()

class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag
        django_get_or_create = ('name',)

    name = factory.Sequence(lambda n: f'tag_{n}')


class SnippetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Snippet
        skip_postgeneration_save = True

    name = factory.Sequence(lambda n: f'snippet_{n}')
    lang = factory.Iterator(['python', 'cpp', 'java', 'javascript'])
    code = factory.Faker('text', max_nb_chars=1000)
    views_count = factory.Faker('random_int', min=0, max=1000)
    public = factory.Faker('boolean')
    user = factory.SubFactory(UserFactory)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            # Если переданы теги, используем их
            for tag in extracted:
                self.tags.add(tag)
        else:
            # Иначе создаем случайные теги
            import random
            num_tags = random.randint(1, 3)
            tags = TagFactory.create_batch(num_tags)
            for tag in tags:
                self.tags.add(tag)


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment
        skip_postgeneration_save = True

    text = factory.Faker('text', max_nb_chars=500)
    author = factory.SubFactory(UserFactory)
    snippet = factory.SubFactory(SnippetFactory)


#
# # Создание отдельных объектов
# user = UserFactory()  # Создает пользователя с именем user_0
# tag = TagFactory()    # Создает тег с именем tag_0
# snippet = SnippetFactory()  # Создает сниппет с пользователем и тегами
# comment = CommentFactory()  # Создает комментарий с автором и сниппетом
#
# # Создание объектов с кастомными данными
# custom_user = UserFactory(username='john_doe', email='john@example.com')
# custom_snippet = SnippetFactory(
#     name='My Python Code',
#     lang='python',
#     code='print("Hello, World!")',
#     public=True
# )

# # Создание нескольких объектов
# users = UserFactory.create_batch(5)  # Создает 5 пользователей
# tags = TagFactory.create_batch(3)    # Создает 3 тега
# snippets = SnippetFactory.create_batch(10)  # Создает 10 сниппетов
#
# # Создание связанных объектов
# user = UserFactory()
# snippet = SnippetFactory(user=user)  # Сниппет принадлежит конкретному пользователю
# comment = CommentFactory(author=user, snippet=snippet)  # Комментарий от того же пользователя
#
# # Работа с тегами
# python_tag = TagFactory(name='python')
# javascript_tag = TagFactory(name='javascript')
# snippet_with_tags = SnippetFactory(tags=[python_tag, javascript_tag])
#
# # Создание сниппета без пользователя (анонимный)
# anonymous_snippet = SnippetFactory(user=None)
#
# # Создание приватного сниппета
# private_snippet = SnippetFactory(public=False)
#
# # Создание сниппета с большим количеством просмотров
# popular_snippet = SnippetFactory(views_count=5000)
#
# # Создание комментария к существующему сниппету
# existing_snippet = SnippetFactory()
# new_comment = CommentFactory(snippet=existing_snippet)
#
# # Создание пользователя с конкретным паролем
# user_with_password = UserFactory()
# user_with_password.set_password('my_secure_password')
