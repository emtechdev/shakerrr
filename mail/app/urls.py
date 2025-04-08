from django.urls import path
from . import views

urlpatterns = [
    # Email Settings URLs
    path('settings/', views.EmailSettingsListView.as_view(), name='settings_list'),
    path('settings/new/', views.EmailSettingsCreateView.as_view(), name='settings_create'),
    path('settings/<int:pk>/edit/', views.EmailSettingsUpdateView.as_view(), name='settings_update'),
    
    # Email Group URLs
    path('', views.EmailGroupListView.as_view(), name='group_list'),
    path('groups/new/', views.EmailGroupCreateView.as_view(), name='group_create'),
    path('groups/<int:pk>/edit/', views.EmailGroupUpdateView.as_view(), name='group_update'),
    path('groups/<int:pk>/delete/', views.EmailGroupDeleteView.as_view(), name='group_delete'),
    
    # Emails URLs
    path('emails/', views.EmailsListView.as_view(), name='email_list'),
    path('emails/new/', views.EmailsCreateView.as_view(), name='email_create'),
    path('emails/<int:pk>/edit/', views.EmailsUpdateView.as_view(), name='email_update'),
    path('emails/<int:pk>/delete/', views.EmailsDeleteView.as_view(), name='email_delete'),

    path('messages/', views.EmailMessageListView.as_view(), name='message_list'),
    path('messages/new/', views.EmailMessageCreateView.as_view(), name='message_create'),
    path('messages/<int:pk>/edit/', views.EmailMessageUpdateView.as_view(), name='message_update'),
    path('messages/<int:pk>/delete/', views.EmailMessageDeleteView.as_view(), name='message_delete'),
    path('messages/<int:pk>/send/', views.send_email_message, name='message_send'),

    path('emails/export/', views.export_emails, name='email_export'),
    path('emails/import/', views.import_emails, name='email_import'),
]