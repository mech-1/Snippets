from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.template.context_processors import request
from django.contrib import auth
from MainApp.models import Snippet, LANG_ICONS
from MainApp.forms import SnippetForm


def get_icon_class(lang):
    return LANG_ICONS.get(lang)


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)

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
    snippets = Snippet.objects.all()
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
    snippet = get_object_or_404(Snippet, pk=id)
    # snippet.views_count += 1
    snippet.views_count = F('views_count') + 1
    snippet.save(update_fields=['views_count'])
    snippet.refresh_from_db()
    context = {'pagename': 'Просмотр сниппета', 'snippet': snippet}
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
            return render(request,'pages/index.html', context=context)

def logout(request):
    auth.logout(request)
    return redirect('home')