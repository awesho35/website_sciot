from django.contrib import admin
from .models import MenuCategory, MenuItem, DrinkCategory, DrinkItem, SpecialMenu


@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_available', 'is_featured']
    list_filter = ['category', 'is_available', 'is_vegetarian', 'is_vegan']
    list_editable = ['price', 'is_available']
    search_fields = ['name', 'description']


@admin.register(DrinkCategory)
class DrinkCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(DrinkItem)
class DrinkItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'volume', 'is_available']
    list_filter = ['category', 'is_available']
    list_editable = ['price', 'is_available']
    search_fields = ['name', 'description']


@admin.register(SpecialMenu)
class SpecialMenuAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'is_active', 'order']
    list_editable = ['price', 'is_active', 'order']
