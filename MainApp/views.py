from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from MainApp.models import Snippet


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    context = {'pagename': 'Добавление нового сниппета'}
    return render(request, 'pages/add_snippet.html', context)


def snippets_page(request):
    snippets = Snippet.objects.all()
    context = {'pagename': 'Просмотр сниппетов', 'snippets': snippets}
    return render(request, 'pages/view_snippets.html', context)


def view_snippet(request, id):
    snippet = get_object_or_404(Snippet, pk=id)
    context = {'pagename': 'Просмотр сниппета', 'snippet': snippet}
    return render(request, 'pages/view_snippet.html', context)
