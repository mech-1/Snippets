import json
import logging

from datetime import datetime
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.http import Http404, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from MainApp.forms import SnippetForm, UserRegistrationForm, CommentForm
from MainApp.models import Snippet, Comment, LANG_CHOICES, Notification
from MainApp.signals import snippet_view
from django.db.models import F, Q, Count, Avg
from MainApp.models import LANG_ICONS

logger = logging.getLogger(__name__)


@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message', '')
        level = data.get('level', 'info')  # Default to 'info' level
        # Map level to Django message levels
        levels = {
            'debug': messages.DEBUG,
            'info': messages.INFO,
            'success': messages.SUCCESS,
            'warning': messages.WARNING,
            'error': messages.ERROR,
        }
        # TODO shows only on page reload
        messages.add_message(request, levels.get(level, messages.INFO), message)
        return JsonResponse({'status': 'success', 'message': 'Message added'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


def snippets_stats(request):
    stats = Snippet.objects.aggregate(total=Count('id'), avg=Avg('id'))
    public = Snippet.objects.filter(public=True).aggregate(total=Count('id'))
    top5 = Snippet.objects.order_by('-views_count').values_list('name', 'views_count')[:5]
    top3user = User.objects.filter(snippet__isnull=False).annotate(created_snippets=Count('snippet__id')).order_by(
        '-created_snippets').values('username', 'created_snippets')[:3]

    context = {
        'pagename': 'Статистика сниппетов',
        'total': stats['total'],
        'total_public': public['total'],
        'avg': stats['avg'],
        'top5': top5,
        'top3user': top3user
    }
    return render(request, 'pages/snippets_stats.html', context)


def index_page(request):
    context = {'pagename': 'PythonBin'}
    # logger.debug("1. Отладочное сообщение")
    # logger.info("2. Info сообщение")
    # logger.error("3. Error сообщение")
    # messages.success(request, "Добро пожаловать на сайт")
    # messages.warning(request, "Доработать закрытие сообщений по таймеру")
    # messages.warning(request, "Доработать закрытие сообщений по таймеру")
    # messages.warning(request, "Доработать закрытие сообщений по таймеру")
    # messages.error(request, f'Error: Ошибка, ! Вы не зарегистрированы.')
    # messages.warning(request, f'Warning: Предупреждение, ! .')
    # messages.success(request, f'Success: Добро пожаловать, ! Вы успешно зарегистрированы.')
    # messages.info(request, f'Info:, ! Вы успешно зарегистрированы.')
    # messages.debug(request, f'Debug: Отладка - дебаг, ! Вы успешно зарегистрированы.')
    return render(request, 'pages/index.html', context)


# sort
# snippets/list
# snippets/list?sort=name
# snippets/list?sort=lang
# snippets/list?sort=-lang
# filters:
# snippets/list?lang=Python&user_id=3

# 1. Сортировка выключена
# 2. Сортировка по возрастанию
# 3. Сортировка по убыванию

# @login_required
# def snippets_my(request):
#     snippets = Snippet.objects.filter(user=request.user)
#     context = {
#         'pagename': 'Мои сниппеты',
#         'snippets': snippets
#     }
#     return render(request, 'pages/view_snippets.html', context)

@login_required
def add_snippet_page(request):
    if request.method == 'GET':
        form = SnippetForm()
        context = {'form': form, "pagename": "Создание сниппета"}
        return render(request, 'pages/add_snippet.html', context)

    if request.method == 'POST':
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.user = request.user
            snippet.save()
            messages.success(request, 'Сниппет успешно добавлен')
            return redirect('snippets-list')
        else:
            errors = ", ".join(form.errors.get('name'))
            messages.error(request, errors)
            context = {'form': form, "pagename": "Создание сниппета"}
            return render(request, 'pages/add_snippet.html', context)


def snippets_page(request, my_snippets, num_snippets_on_page=5):
    if my_snippets:
        if not request.user.is_authenticated:
            raise PermissionDenied
        pagename = 'Мои сниппеты'
        snippets = Snippet.objects.filter(user=request.user)
    else:
        pagename = 'Просмотр сниппетов'
        if request.user.is_authenticated:  # auth: all public + self private
            snippets = Snippet.objects.filter(Q(public=True) | Q(public=False, user=request.user))
        else:  # not auth: all public
            snippets = Snippet.objects.filter(public=True)

    # search
    search = request.GET.get("search")
    if search:
        snippets = snippets.filter(
            Q(name__icontains=search) |
            Q(code__icontains=search)
        )

    # filter
    lang = request.GET.get("lang")
    if lang:
        snippets = snippets.filter(lang=lang)

    user_id = request.GET.get("user_id")
    if user_id:
        snippets = snippets.filter(user__id=user_id)

    # sort
    sort = request.GET.get("sort")
    if sort:
        snippets = snippets.order_by(sort)

    # TODO: работает или пагинация или сортировка по полю!
    paginator = Paginator(snippets, num_snippets_on_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # users = User.objects.filter(snippet__isnull=False).distinct()
    # users = User.objects.filter(snippet__isnull=False).annotate(snippets_count=Count('snippet'))
    users = User.objects.filter(snippet__isnull=False).annotate(snippets_count=Count('snippet__id'))
    context = {
        'pagename': pagename,
        'page_obj': page_obj,
        'sort': sort,
        'LANG_CHOICES': LANG_CHOICES,
        'users': users,
        'lang': lang,
        'user_id': user_id
    }
    return render(request, 'pages/view_snippets.html', context)


def snippet_detail(request, id):
    # snippet = get_object_or_404(Snippet, id=id)
    snippet = Snippet.objects.prefetch_related("comments").get(id=id)
    # snippet.views_count = F('views_count') + 1
    # snippet.save(update_fields=["views_count"])  # -> SET v_c = 11 | SET v_c =  v_c + 1
    # snippet.refresh_from_db()
    # Отправляем сигнал
    snippet_view.send(sender=snippet.__class__, snippet=snippet)
    comments = snippet.comments.all()
    comment_form = CommentForm()
    context = {
        'pagename': f'Сниппет: {snippet.name}',
        'snippet': snippet,
        'comments': comments,
        'comment_form': comment_form
    }
    return render(request, 'pages/snippet_detail.html', context)


# Удалять сниппеты только принадлежащие пользователю
# 404 not found
# 403 permission denied
# 302 redirect
def snippet_delete(request, id):
    snippet = get_object_or_404(Snippet, id=id)
    if snippet.user != request.user:
        raise PermissionDenied()
    snippet.delete()
    messages.success(request, 'Сниппет успешно удален')

    return redirect('snippets-list')


def snippet_edit(request, id):
    if request.method == "GET":
        snippet = get_object_or_404(Snippet, id=id)
        form = SnippetForm(instance=snippet)
        context = {
            "pagename": "Редактировать Сниппет",
            "form": form,
            "edit": True,
            "id": id
        }
        return render(request, 'pages/add_snippet.html', context)

    if request.method == "POST":
        snippet = get_object_or_404(Snippet, id=id)
        form = SnippetForm(request.POST, instance=snippet)
        if form.is_valid():
            form.save()
            messages.success(request, 'Сниппет успешно отредактирован')

        return redirect('snippets-list')


def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            context = {
                "errors": ["Неверные username или password"],
                "username": username
            }
            return render(request, "pages/index.html", context)


def user_logout(request):
    auth.logout(request)
    return redirect('home')


def user_registration(request):
    if request.method == "GET":  # page with form
        form = UserRegistrationForm()
        context = {
            "form": form
        }
        return render(request, "pages/registration.html", context)

    if request.method == "POST":  # form data
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Пользователь {user.username} успешно зарегистрирован!")
            return redirect('home')
        else:
            context = {
                "form": form
            }
            return render(request, "pages/registration.html", context)


# 302 redirect on success or anonymous (redirect to login - @login_required)
# 404 method on get request
@login_required
def comment_add(request):
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        snippet_id = request.POST.get('snippet_id')  # Получаем ID сниппета из формы
        snippet = get_object_or_404(Snippet, id=snippet_id)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user  # Текущий авторизованный пользователь
            comment.snippet = snippet
            comment.save()
            messages.success(request, 'Комментарий успешно добавлен')

        return redirect('snippet-detail', id=snippet_id)
    raise Http404


@login_required
def user_notifications(request):
    """Страница с уведомлениями пользователя"""

    # Получаем все уведомления для авторизованного пользователя, сортируем по дате создания
    notifications = Notification.objects.filter(recipient=request.user)

    # Отмечаем все уведомления как прочитанные при переходе на страницу
    Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)

    context = {
        'pagename': 'Мои уведомления',
        'notifications': notifications,
    }
    return render(request, 'pages/notifications.html', context)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def simple_api_view(request):
    """
    Простой API endpoint для обработки GET и POST запросов
    """

    if request.method == 'GET':
        # Обработка GET запроса
        try:
            # Здесь может быть логика получения данных из базы
            data = {
                'success': True,
                'message': 'Данные успешно получены!',
                'timestamp': str(datetime.now()),
                'items': [
                    {'id': 1, 'name': 'Элемент 1'},
                    {'id': 2, 'name': 'Элемент 2'},
                    {'id': 3, 'name': 'Элемент 3'}
                ]
            }
            return JsonResponse(data)

        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)

    elif request.method == 'POST':
        # Обработка POST запроса
        try:
            # Парсим JSON данные из запроса
            data = json.loads(request.body)

            # Обрабатываем полученные данные
            received_message = data.get('message', '')

            # Здесь может быть логика сохранения в базу данных

            response_data = {
                'success': True,
                'message': f'Получено сообщение: {received_message}',
                'processed': True
            }

            return JsonResponse(response_data)

        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Неверный формат JSON'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)


def api_test_page(request):
    return render(request, "pages/api_test.html")


@login_required
def unread_notifications_count(request):
    """
    API endpoint для получения количества непрочитанных уведомлений
    Использует long polling - отвечает только если есть непрочитанные уведомления
    """
    import time

    # Максимальное время ожидания (30 секунд)
    max_wait_time = 30
    check_interval = 1  # Проверяем каждую секунду
    last_count = int(request.GET.get('last_count', 0))

    start_time = time.time()
    unread_count = 0

    while time.time() - start_time < max_wait_time:
        # Получаем количество непрочитанных уведомлений
        unread_count = Notification.objects.filter(
            recipient=request.user,
            is_read=False
        ).count()

        # Если есть непрочитанные уведомления, сразу отвечаем
        if unread_count > last_count:
            return JsonResponse({
                'success': True,
                'unread_count': unread_count,
                'timestamp': str(datetime.now())
            })

        # Ждем перед следующей проверкой
        time.sleep(check_interval)

    # Если время истекло и нет уведомлений, возвращаем 0
    return JsonResponse({
        'success': True,
        'unread_count': last_count,
        'timestamp': str(datetime.now())
    })


def is_authenticated(request):
    if request.user.is_authenticated:
        return JsonResponse({'is_authenticated': True})
    else:
        return JsonResponse({'is_authenticated': False})