from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django.contrib import messages, auth
from MainApp.forms import SnippetForm, CommentForm
from MainApp.models import Snippet, LANG_CHOICES


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


class SnippetsListView(ListView):
    """Отображение списка сниппетов с фильтрацией, поиском и сортировкой"""
    model = Snippet
    template_name = 'pages/view_snippets.html'
    context_object_name = 'snippets'
    paginate_by = 4

    def get_queryset(self):
        my_snippets = self.kwargs.get('my_snippets', False)

        if my_snippets:
            if not self.request.user.is_authenticated:
                raise PermissionDenied
            queryset = Snippet.objects.filter(user=self.request.user)
        else:
            if self.request.user.is_authenticated:  # auth: all public + self private
                queryset = Snippet.objects.filter(
                    Q(public=True) | Q(public=False, user=self.request.user)
                ).select_related("user")
            else:  # not auth: all public
                queryset = Snippet.objects.filter(public=True).select_related("user")

        # Поиск
        search = self.request.GET.get("search")
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(code__icontains=search)
            )

        # Фильтрация по языку
        lang = self.request.GET.get("lang")
        if lang:
            queryset = queryset.filter(lang=lang)

        # Фильтрация по пользователю
        user_id = self.request.GET.get("user_id")
        if user_id:
            queryset = queryset.filter(user__id=user_id)

        # Сортировка
        sort = self.request.GET.get("sort")
        if sort:
            queryset = queryset.order_by(sort)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        my_snippets = self.kwargs.get('my_snippets', False)

        if my_snippets:
            context['pagename'] = 'Мои сниппеты'
        else:
            context['pagename'] = 'Просмотр сниппетов'

        # Получаем пользователей со сниппетами
        users = User.objects.filter(snippet__isnull=False).distinct()

        context.update({
            'sort': self.request.GET.get("sort"),
            'LANG_CHOICES': LANG_CHOICES,
            'users': users,
            'lang': self.request.GET.get("lang"),
            'user_id': self.request.GET.get("user_id")
        })

        return context


# def snippets_page(request, my_snippets, num_snippets_on_page=5):
#     if my_snippets:
#         if not request.user.is_authenticated:
#             raise PermissionDenied
#         pagename = 'Мои сниппеты'
#         # selected_related can stay before or after filter
#         snippets = Snippet.objects.select_related('user').filter(user=request.user)
#     else:
#         pagename = 'Просмотр сниппетов'
#         if request.user.is_authenticated:  # auth: all public + self private
#             snippets = Snippet.objects.select_related('user').filter(Q(public=True) | Q(public=False, user=request.user))
#         else:  # not auth: all public
#             snippets = Snippet.objects.filter(public=True).select_related('user')
#
#     # search
#     search = request.GET.get("search")
#     if search:
#         snippets = snippets.filter(
#             Q(name__icontains=search) |
#             Q(code__icontains=search)
#         )
#
#     # filter
#     lang = request.GET.get("lang")
#     if lang:
#         snippets = snippets.filter(lang=lang)
#
#     user_id = request.GET.get("user_id")
#     if user_id:
#         snippets = snippets.filter(user__id=user_id)
#
#     # sort
#     sort = request.GET.get("sort")
#     if sort:
#         snippets = snippets.order_by(sort)
#
#     # TODO: работает или пагинация или сортировка по полю!
#     paginator = Paginator(snippets, num_snippets_on_page)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     # users = User.objects.filter(snippet__isnull=False).distinct()
#     # users = User.objects.filter(snippet__isnull=False).annotate(snippets_count=Count('snippet'))
#     users = User.objects.filter(snippet__isnull=False).annotate(snippets_count=Count('snippet__id'))
#     context = {
#         'pagename': pagename,
#         'page_obj': page_obj,
#         'sort': sort,
#         'LANG_CHOICES': LANG_CHOICES,
#         'users': users,
#         'lang': lang,
#         'user_id': user_id
#     }
#     return render(request, 'pages/view_snippets.html', context)


class SnippetEditView(LoginRequiredMixin, UpdateView):
    model = Snippet
    form_class = SnippetForm
    template_name = 'pages/add_snippet.html'
    success_url = reverse_lazy('snippets-list')
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pagename'] = 'Редактировать Сниппет'
        # form add automatically
        context['edit'] = True
        context['id'] = self.kwargs.get('id')
        return context

# def snippet_edit(request, id):
#     if request.method == "GET":
#         snippet = get_object_or_404(Snippet, id=id)
#         form = SnippetForm(instance=snippet)
#         context = {
#             "pagename": "Редактировать Сниппет",
#             "form": form,
#             "edit": True,
#             "id": id
#         }
#         return render(request, 'pages/add_snippet.html', context)
#
#     if request.method == "POST":
#         snippet = get_object_or_404(Snippet, id=id)
#         form = SnippetForm(request.POST, instance=snippet)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Сниппет успешно отредактирован')
#
#         return redirect('snippets-list')
