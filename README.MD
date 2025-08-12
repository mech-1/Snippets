python3 -m venv .venv
source .venv/bin/activate
pip install django

cd ~/projects/DjangoCountries
Создание проекта Django в текущем каталоге:
django-admin startproject DjangoCountries .
#django-admin startproject mysite djangotutorial

Создайте новое приложение внутри вашего проекта:
python manage.py startapp MainApp

PYTHONUNBUFFERED=1;DJANGO_SETTINGS_MODULE=DjangoCountries.settings


install requirements: 
`pip install -r requirements.txt`

run project:
`python manage.py runserver`

run django-extensions console: 
`python manage.py shell_plus --ipython`


snippets = Snippet.objects.filter(name__icontains='basic')

snippets = Snippet.objects.filter(user__username='user3')

headline__startswith

In [12]: snippets = Snippet.objects.filter(public=True).order_by('-views_count')[:5]

snippets = Snippet.objects.filter(Q(lang='python') | Q(lang='javascript'))
snippets = Snippet.objects.filter(Q(lang='python') | Q(lang='javascript'))
snippets = Snippet.objects.filter((Q(lang='python') | Q(lang='javascript')) & Q(public=False))

snippets = Snippet.objects.filter(lang__in=['python', 'javascript'])

snippets = Snippet.objects.filter(lang__in=['python', 'javascript'])
snippets = Snippet.objects.filter(public=False).filter(lang__in=['python', 'javascript'])

In [13]: snippets = Snippet.objects.filter(views_count__gt=150)

In [15]: comments = Comment.objects.filter(snippet__lang='cpp')

In [19]: for comment in comments:
    ...:     print(comment.snippet.lang)
 
In [22]: snippets_count = Snippet.objects.filter(user__username='user3').count()
In [21]: print(snippets)

In [23]: count_comments = Comment.objects.filter(snippet__name='Python: Hello World').count()

In [33]: comments_names = Comment.objects.filter(snippet__id=1).values('author__username')

In [39]: users = User.objects.filter(snippet__isnull=False).distinct()

'snippet' - model name lowercase when not exist relative_name
users_with_snippet_count = User.objects.annotate(snippet_count=Count('snippet'))

num_users_snippet = User.objects.all().annotate(num_snippets=Count('snippet'))

for user in num_users_snippet:
   ...:     print(user,user.num_snippets)
 
views = Snippet.objects.aggregate(Max('views_count'))
stats = Snippet.objects.aggregate(max_views=Max('views_count'))
print(stats['max_views'])
220

print(stats)
{'max_views': 220}

print(stats['max_views'])
220

stats = Snippet.objects.aggregate(avg_views=Avg('views_count'))

In [16]: public_comments = Comment.objects.filter(snippet__public=False).aggregate(Count('snippet__id'))
DEBUG (0.003) SELECT COUNT("MainApp_comment"."snippet_id") AS "snippet__id__count" FROM "MainApp_comment" INNER JOIN "MainApp_snippet" ON ("MainApp_comment"."snippet_id" = "MainApp_snippet"."id") WHERE NOT "MainApp_snippet"."public"; args=(); alias=default (Duration: 0.003s)

In [17]: print(public_comments)
{'snippet__id__count': 3}

public_comments = Comment.objects.filter(snippet__public=False).count()
DEBUG (0.002) SELECT COUNT(*) AS "__count" FROM "MainApp_comment" INNER JOIN "MainApp_snippet" ON ("MainApp_comment"."snippet_id" = "MainApp_snippet"."id") WHERE NOT "MainApp_snippet"."public"; args=(); alias=default (Duration: 0.002s)

In [21]: print(public_comments)
3


In [28]: stats = Snippet.objects.filter(public=True).aggregate(total_comments = Count('comments__id'))

In [29]: stats
Out[29]: {'total_comments': 45}

print(stats['total_comments'])
45
Number public comments:
comments_count = Comment.objects.filter(snippet__public=True).count()
comments_count = Comment.objects.filter(snippet__public=True).aggregate(Count('id'))
In [39]: comments_count = Comment.objects.filter(snippet__public=True).aggregate(Total=Count('id'))
In [40]: print(comments_count)
{'Total': 45}
max and min dates snippets creation date
In [41]: stats = Snippet.objects.aggregate(min_date=Min('creation_date'),max_date=Max('creation_date'))
top5 comments:
In [44]: top5 = Snippet.objects.annotate(comments_count=Count('comments')).order_by('-comments_count')[:5]

(.venv) ijn@MacBook-Air-Evgenij Snippets % pip install pytest-django    

(.venv) ijn@MacBook-Air-Evgenij Snippets % pytest -v MainApp/test_views.py::TestAddSnippetPage

pip install factory-boy
pip freeze > requirements.txt 

(.venv) ijn@MacBook-Air-Evgenij Snippets % pip install pytest-cov 
(.venv) ijn@MacBook-Air-Evgenij Snippets % pytest --cov .
(.venv) ijn@MacBook-Air-Evgenij Snippets % pytest --cov=. --cov-report=html
pip install pytest pytest-django selenium webdriver-manager

(.venv) ijn@MacBook-Air-Evgenij Snippets % python manage.py shell_plus --ipython
IPython 8.37.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: comment = Comment.objects.get(id=1)

In [2]: comment.text
Out[2]: 'Отличный способ начать! Просто и понятно.'

In [3]: comment.snippet.name
Out[3]: 'Python: Hello World'

In [4]: user = User.objects.get(id=1)

In [5]: user.username
Out[5]: 'user1'

In [6]: LikeDislike.objects.create(user=user, vote=1, content_object=comment)
Out[6]: <LikeDislike: LikeDislike object (1)>


In [7]: LikeDislike.objects.create(user=user, vote=1, content_object=comment)
---------------------------------------------------------------------------
IntegrityError                            Traceback (most recent call last)
IntegrityError: UNIQUE constraint failed: MainApp_likedislike.user_id, MainApp_likedislike.content_type_id, MainApp_likedislike.object_id


In [9]: user2 = User.objects.get(id=2)

In [10]: LikeDislike.objects.create(user=user2, vote=1, content_object=comment)
Out[10]: <LikeDislike: LikeDislike object (2)>


In [11]: user3 = User.objects.get(id=3)

In [12]: LikeDislike.objects.create(user=user3, vote=-1, content_object=comment)
Out[12]: <LikeDislike: LikeDislike object (3)>

In [13]: comment.likes.filter(vote=1).count()
    ...: 
Out[13]: 2

In [14]: comment.likes.filter(vote=-1).count()
Out[14]: 1

In [15]: comment.likes.filter(vote=LikeDislike.DISLIKE).count()
Out[15]: 1

In [16]: comment.likes.filter(vote=LikeDislike.LIKE).count()
Out[16]: 2
