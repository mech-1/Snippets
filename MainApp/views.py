from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from MainApp.models import Snippet, Comment
from MainApp.forms import SnippetForm, UserRegistrationForm, CommentForm
from django.db.models import F, Q
from MainApp.models import LANG_ICONS
from django.contrib import auth
from django.contrib.auth.decorators import login_required


def get_icon_class(lang):
    return LANG_ICONS.get(lang)


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


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
            return redirect('snippets-list')
        else:
            context = {'form': form, "pagename": "Создание сниппета"}
            return render(request, 'pages/add_snippet.html', context)


# snippets/list
# snippets/list?sort=name
# snippets/list?sort=lang
# snippets/list?sort=-lang

# 1. Сортировка выключена
# 2. Сортировка по возрастанию
# 3. Сортировка по убыванию

def snippets_page(request):
    if request.user.is_authenticated:  # auth: all public + self private
        snippets = Snippet.objects.filter(Q(public=True) | Q(public=False, user=request.user))
    else:  # not auth: all public
        snippets = Snippet.objects.filter(public=True)

    # sort
    sort = request.GET.get("sort")
    if sort:
        snippets = snippets.order_by(sort)

    for snippet in snippets:
        snippet.icon_class = get_icon_class(snippet.lang)
    context = {
        'pagename': 'Просмотр сниппетов',
        'snippets': snippets,
        'sort': sort
    }
    return render(request, 'pages/view_snippets.html', context)


def snippets_my(request):
    snippets = Snippet.objects.filter(user=request.user)
    context = {
        'pagename': 'Мои сниппеты',
        'snippets': snippets
    }
    return render(request, 'pages/view_snippets.html', context)


def snippet_detail(request, id):
    # snippet = get_object_or_404(Snippet, id=id)
    snippet = Snippet.objects.prefetch_related("comments").get(id=id)
    snippet.views_count = F('views_count') + 1
    snippet.save(update_fields=["views_count"])  # -> SET v_c = 11 | SET v_c =  v_c + 1
    snippet.refresh_from_db()
    comments = snippet.comments.all()
    comment_form = CommentForm()
    context = {
        'pagename': f'Сниппет: {snippet.name}',
        'snippet': snippet,
        'comments': comments,
        'comment_form': comment_form
    }
    return render(request, 'pages/snippet_detail.html', context)


def snippet_delete(request, id):
    snippet = get_object_or_404(Snippet, id=id)
    snippet.delete()

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
            form.save()
            return redirect('home')
        else:
            context = {
                "form": form
            }
            return render(request, "pages/registration.html", context)


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

        return redirect('snippet-detail', id=snippet_id)
    raise Http404