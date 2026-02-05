from django.contrib import admin
from .models import MediaCategory, MediaImage, CarouselSlide, HeroBanner


@admin.register(MediaCategory)
class MediaCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(MediaImage)
class MediaImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'width', 'height', 'uploaded_at']
    list_filter = ['category', 'uploaded_at']
    search_fields = ['title', 'alt_text']


@admin.register(CarouselSlide)
class CarouselSlideAdmin(admin.ModelAdmin):
    list_display = ['title', 'order', 'is_active']
    list_editable = ['order', 'is_active']


@admin.register(HeroBanner)
class HeroBannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']
    list_editable = ['is_active']
