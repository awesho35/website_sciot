from django.urls import path
from . import views

app_name = 'admin_custom'

urlpatterns = [
    # Auth
    path('login/', views.admin_login, name='login'),
    path('logout/', views.admin_logout, name='logout'),
    
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Events
    path('events/', views.events_list, name='events'),
    path('events/calendar/', views.events_calendar, name='events_calendar'),
    path('events/create/', views.event_create, name='event_create'),
    path('events/<int:pk>/edit/', views.event_edit, name='event_edit'),
    path('events/<int:pk>/delete/', views.event_delete, name='event_delete'),
    path('events/categories/', views.event_categories, name='event_categories'),
    
    # Menu
    path('menu/', views.menu_list, name='menu'),
    path('menu/items/create/', views.menu_item_create, name='menu_item_create'),
    path('menu/items/<int:pk>/edit/', views.menu_item_edit, name='menu_item_edit'),
    path('menu/items/<int:pk>/delete/', views.menu_item_delete, name='menu_item_delete'),
    path('menu/categories/', views.menu_categories, name='menu_categories'),
    path('menu/drinks/', views.drinks_list, name='drinks'),
    
    # Media
    path('media/', views.media_gallery, name='media'),
    path('media/upload/', views.media_upload, name='media_upload'),
    path('media/<int:pk>/delete/', views.media_delete, name='media_delete'),
    path('media/carousel/', views.carousel_manage, name='carousel'),
    
    # Settings
    path('settings/', views.site_settings, name='settings'),
    path('settings/social/', views.social_links, name='social_links'),
    
    # Messages
    path('messages/', views.contact_messages, name='messages'),
    path('messages/<int:pk>/', views.message_detail, name='message_detail'),
    
    # API endpoints for AJAX
    path('api/events/', views.api_events, name='api_events'),
    path('api/events/calendar/', views.api_events_calendar, name='api_events_calendar'),
    path('api/events/<int:pk>/', views.api_event_detail, name='api_event_detail'),
]
