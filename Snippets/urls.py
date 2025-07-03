from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views

urlpatterns = [
    path('', views.index_page, name='home'),
    path('snippets/add', views.add_snippet_page, name='add_snippet'),
    path('snippets/my', views.snippets_my, name='snippets_my'),
    path('snippets/list', views.snippets_page, name='snippets_list'),
    path('snippet/<int:id>', views.view_snippet, name='view_snippet'),
    path('snippet/<int:id>/edit', views.snippet_edit, name='snippet_edit'),
    path('snippet/<int:id>/delete', views.snippet_delete, name='snippet_delete'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
]
