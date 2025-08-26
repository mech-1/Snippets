from django.urls import path
from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views, views_cbv
from django.contrib import admin
urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', views.index_page, name="home"),
    # path('comment/<int:id>/liked', views.comment_like, {'vote': 1}, name="comment-like"),
    # path('comment/<int:id>/disliked', views.comment_like, {'vote': -1}, name="comment-dislike"),
    # path('snippets/add', views.add_snippet_page, name="snippet-add"),
    path('snippets/add', views_cbv.AddSnippetView.as_view(), name="snippet-add"),
    path('snippets/list', views.snippets_page, {'my_snippets': False}, name="snippets-list"),
    path('snippets/my', views.snippets_page, {'my_snippets': True}, name="snippets-my"),
    path('snippets/list', views_cbv.SnippetsListView.as_view(), {'my_snippets': False}, name="snippets-list"),
    path('snippets/my', views_cbv.SnippetsListView.as_view(), {'my_snippets': True}, name="snippets-my"),
    path('snippets/stats', views.snippets_stats, name="snippets-stats"),
    # path('snippet/<int:id>', views.snippet_detail, name="snippet-detail"),
    path('snippet/<int:id>', views_cbv.SnippetDetailView.as_view(), name="snippet-detail"),
    # path('snippet/<int:id>/edit', views.snippet_edit, name="snippet-edit"),
    path('snippet/<int:id>/edit', views_cbv.SnippetEditView.as_view(), name="snippet-edit"),
    path('snippet/<int:id>/delete', views.snippet_delete, name="snippet-delete"),
    path('snippet/subscribe', views.snippet_subscribe, name='snippet-subscribe'),
    path('snippet/unsubscribe', views.snippet_unsubscribe, name='snippet-unsubscribe'),
    path('login', views.login, name="login"),
    # path('logout', views.user_logout, name='logout'),
    path('logout', views_cbv.UserLogoutView.as_view(), name='logout'),
    path('registration', views.user_registration, name='registration'),
    path('registration', views_cbv.UserRegistration.as_view(), name='registration'),
    path('comment/add', views.comment_add, name="comment_add"),
    path('send-message/', views.send_message, name='send_message'),
    path('notifications/', views.user_notifications, name="notifications"),
    path('notification/<int:id>/delete', views.notification_delete, name="notification-delete"),
    path('notifications/delete-read', views.notifications_delete_read, name="notifications-delete-read"),
    path('profile', views.user_profile, name="profile"),
    path('profile/edit', views.edit_profile, name="edit-profile"),
    path('password/change', views.password_change, name="password_change"),
    path('activate/<int:user_id>/<str:token>/', views.activate_account, name='activate_account'),
    path('resend_email', views.resend_email, name="resend-email"),
    # API endpoints
    path('api/simple-data/', views.simple_api_view, name='simple_api'),
    path('api-page/', views.api_test_page, name='apt-test-page'),
    path('api/notifications/unread-count/', views.unread_notifications_count, name='unread_notifications_count'),
    path('api/is_authenticated', views.is_authenticated, name="unread_notifications_count"),
    path('api/comment/like', views.add_comment_like, name="add_comment_like"),

] + debug_toolbar_urls()

# if settings.DEBUG:
#    import debug_toolbar
#
#    urlpatterns += [
#        path('__debug__/', include(debug_toolbar.urls))
#    ]
# ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# url: snippet/2/delete
# /comment/3/like
# /comment/2/dislike