from django.contrib import admin
from .models import Page, ContentSection, FAQ


class ContentSectionInline(admin.TabularInline):
    model = ContentSection
    extra = 0


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'is_published', 'show_in_menu', 'menu_order']
    list_editable = ['is_published', 'show_in_menu', 'menu_order']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ContentSectionInline]


@admin.register(ContentSection)
class ContentSectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'section_type', 'page', 'order']
    list_filter = ['section_type', 'page']
    list_editable = ['order']


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'order', 'is_published']
    list_filter = ['category', 'is_published']
    list_editable = ['order', 'is_published']
