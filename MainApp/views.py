from django.contrib.auth.decorators import login_required
from django.db.models import F, Q
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.template.context_processors import request
from django.contrib import auth
from MainApp.models import Snippet, LANG_ICONS, Comment
from MainApp.forms import SnippetForm, UserRegistrationForm, CommentForm
from django.contrib.auth.forms import UserCreationForm


def get_icon_class(lang):
    return LANG_ICONS.get(lang)


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def user_registration(request):
    context = {'pagename': 'Регистрация нового пользователя'}
    if request.method == 'GET':
        form = UserRegistrationForm()
        context = {'pagename': 'Регистрация нового пользователя', 'form': form}

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            context = {"pagename": "Регистрация нового пользователя", 'form': form}
    return render(request, 'pages/registration.html', context)


@login_required()
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

        return redirect('view_snippet',
                        id=snippet_id)  # Предполагаем, что у вас есть URL для деталей сниппета с параметром pk

    raise Http404


@login_required
def add_snippet_page(request):
    # form = SnippetForm(request.POST or None)
    if request.method == 'GET':
        form = SnippetForm()
        context = {'pagename': 'Добавление нового сниппета', 'form': form}
        return render(request, 'pages/add_snippet.html', context)
    if request.method == 'POST':
        form = SnippetForm(request.POST)
        if form.is_valid():
            # name = form.cleaned_data['name']
            # lang = form.cleaned_data['lang']
            # code = form.cleaned_data['code']
            # # save object Snippet to db
            # Snippet.objects.create(name=name, lang=lang, code=code)
            snippet = form.save(commit=False)
            snippet.user = request.user
            snippet.save()
            return redirect('snippets_list')
        else:
            context = {'form': form, "pagename": "Создание сниппета"}
            return render(request, 'pages/add_snippet.html', context)


def snippet_edit(request, id):
    if request.method == 'GET':
        form = SnippetForm(instance=get_object_or_404(Snippet, pk=id))
        context = {'pagename': 'Редактирование сниппета', 'form': form, 'edit': True, 'id': id}
        return render(request, 'pages/add_snippet.html', context)
    if request.method == 'POST':
        form = SnippetForm(request.POST, instance=get_object_or_404(Snippet, pk=id))
        form.save()
    return redirect('snippets_list')


def snippets_page(request):
    if request.user.is_authenticated:  # auth: all public + self.private
        snippets = Snippet.objects.all().filter(Q(public=True) | Q(public=False, user=request.user))
    else:
        snippets = Snippet.objects.all().filter(public=True)

    for snippet in snippets:
        snippet.icon_class = get_icon_class(snippet.lang)
    context = {'pagename': 'Просмотр сниппетов', 'snippets': snippets}
    return render(request, 'pages/view_snippets.html', context)


def snippets_my(request):
    snippets = Snippet.objects.filter(user=request.user)
    # snippets = Snippet.objects.filter(user_id=request.user.id)
    for snippet in snippets:
        snippet.icon_class = get_icon_class(snippet.lang)
    context = {'pagename': 'Мои сниппеты', 'snippets': snippets}
    return render(request, 'pages/view_snippets.html', context)


def view_snippet(request, id):
    # snippet = get_object_or_404(Snippet, pk=id)
    snippet = Snippet.objects.prefetch_related('comments').get(id=id)
    # snippet.views_count += 1
    snippet.views_count = F('views_count') + 1
    snippet.save(update_fields=['views_count'])
    snippet.refresh_from_db()
    snippets = Snippet.objects.all().filter(Q(public=True) | Q(public=False, user=request.user))
    # comments = Comment.objects.filter(snippet=snippet)  # Получаем все комментарии для данного сниппета
    comments = snippet.comments.all()
    comment_form = CommentForm()  # Передаем пустую форму для добавления комментариев

    context = {'pagename': 'Просмотр сниппета', 'snippet': snippet, 'comments': comments,
               'comment_form': comment_form}
    return render(request, 'pages/view_snippet.html', context)


def snippet_delete(request, id):
    snippet = get_object_or_404(Snippet, pk=id)
    snippet.delete()
    return redirect('snippets_list')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            context = {
                "errors": ["Неверные usernanem или password"],
                "username": username,
            }
            return render(request, 'pages/index.html', context=context)


def logout(request):
    auth.logout(request)
    return redirect('home')
