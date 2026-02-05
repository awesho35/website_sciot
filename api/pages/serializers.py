from rest_framework import serializers
from .models import Page, ContentSection, FAQ


class ContentSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentSection
        fields = '__all__'


class PageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ['id', 'title', 'slug', 'is_published', 'show_in_menu', 'menu_order']


class PageDetailSerializer(serializers.ModelSerializer):
    sections = ContentSectionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Page
        fields = '__all__'


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'
