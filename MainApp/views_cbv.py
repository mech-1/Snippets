from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView
from django.contrib import messages, auth
from MainApp.forms import SnippetForm, CommentForm
from MainApp.models import Snippet


class AddSnippetView(LoginRequiredMixin, CreateView):
    """Создание нового сниппета"""
    model = Snippet
    form_class = SnippetForm
    template_name = 'pages/add_snippet.html'
    success_url = reverse_lazy('snippets-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pagename'] = 'Создание сниппета'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Success!!!")
        return super().form_valid(form)
    # original function view
    # @login_required
    # def add_snippet_page(request):
    #     if request.method == 'GET':
    #         form = SnippetForm()
    #         context = {'form': form, "pagename": "Создание сниппета"}
    #         return render(request, 'pages/add_snippet.html', context)
    #
    #     if request.method == 'POST':
    #         form = SnippetForm(request.POST)
    #         if form.is_valid():
    #             snippet = form.save(commit=False)
    #             snippet.user = request.user
    #             snippet.save()
    #             messages.success(request, "Success!!!")
    #             return redirect('snippets-list')
    #         else:
    #             context = {'form': form, "pagename": "Создание сниппета"}
    #             return render(request, 'pages/add_snippet.html', context)


class SnippetDetailView(DetailView):
    model = Snippet
    # queryset = Snippet.objects.prefetch_related("comments").all()
    template_name = 'pages/snippet_detail.html'
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        snippet = self.get_object()
        context['pagename'] = f'Сниппет: {snippet.name}'
        # or comments get in template {{ snippet.comments.all }}
        context['comments'] = snippet.comments.all()
        context['comment_form'] = CommentForm()
        return context

    def get_queryset(self):
        return Snippet.objects.prefetch_related("comments")


# def snippet_detail(request, id):
#     # snippet = get_object_or_404(Snippet, id=id)
#     snippet = Snippet.objects.prefetch_related("comments").get(id=id)
#     # snippet.views_count = F('views_count') + 1
#     # snippet.save(update_fields=["views_count"])  # -> SET v_c = 11 | SET v_c =  v_c + 1
#     # snippet.refresh_from_db()
#     # Отправляем сигнал
#     snippet_view.send(sender=snippet.__class__, snippet=snippet)
#     comments = snippet.comments.all()
#     # comments = comments.annotate(like_count=Count('likes', filter=Q(likes__vote=LikeDislike.LIKE)))
#     comment_form = CommentForm()
#     context = {
#         'pagename': f'Сниппет: {snippet.name}',
#         'snippet': snippet,
#         'comments': comments,
#         'comment_form': comment_form
#     }
#     return render(request, 'pages/snippet_detail.html', context)


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        auth.logout(request)
        return redirect('home')
# def user_logout(request):
#     auth.logout(request)
#     return redirect('home')
