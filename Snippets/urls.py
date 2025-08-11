from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views
from django.contrib import admin
urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.index_page, name="home"),
    path('snippets/add', views.add_snippet_page, name="snippet-add"),
    path('snippets/list', views.snippets_page, {'my_snippets': False}, name="snippets-list"),
    path('snippets/my', views.snippets_page, {'my_snippets': True}, name="snippets-my"),
    path('snippets/stats', views.snippets_stats, name="snippets-stats"),
    path('snippet/<int:id>', views.snippet_detail, name="snippet-detail"),
    path('snippet/<int:id>/delete', views.snippet_delete, name="snippet-delete"),
    path('snippet/<int:id>/edit', views.snippet_edit, name="snippet-edit"),
    path('login', views.login, name="login"),
    path('logout', views.user_logout, name='logout'),
    path('registration', views.user_registration, name='registration'),
    path('comment/add', views.comment_add, name="comment_add"),
    path('send-message/', views.send_message, name='send_message'),
    path('notifications/', views.user_notifications, name="notifications"),
    # API endpoints
    path('api/simple-data/', views.simple_api_view, name='simple_api'),
    path('api-page/', views.api_test_page, name='apt-test-page'),
    path('api/notifications/unread-count/', views.unread_notifications_count, name='unread_notifications_count'),
]
# url: snippet/2/delete