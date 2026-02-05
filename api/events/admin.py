from django.contrib import admin
from .models import Event, EventCategory


@admin.register(EventCategory)
class EventCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'start_time', 'category', 'status', 'is_featured']
    list_filter = ['status', 'category', 'is_featured', 'date']
    search_fields = ['title', 'description', 'artist_name']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'date'
