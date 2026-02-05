from rest_framework import serializers
from .models import MenuCategory, MenuItem, DrinkCategory, DrinkItem, SpecialMenu


class MenuItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = MenuItem
        fields = '__all__'


class MenuCategorySerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True, read_only=True)
    items_count = serializers.SerializerMethodField()
    
    class Meta:
        model = MenuCategory
        fields = ['id', 'name', 'slug', 'description', 'icon', 'order', 'is_active', 'items', 'items_count']
    
    def get_items_count(self, obj):
        return obj.items.filter(is_available=True).count()


class MenuCategoryListSerializer(serializers.ModelSerializer):
    """Version légère pour les listes"""
    items_count = serializers.SerializerMethodField()
    
    class Meta:
        model = MenuCategory
        fields = ['id', 'name', 'slug', 'description', 'icon', 'order', 'is_active', 'items_count']
    
    def get_items_count(self, obj):
        return obj.items.filter(is_available=True).count()


class DrinkItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        model = DrinkItem
        fields = '__all__'


class DrinkCategorySerializer(serializers.ModelSerializer):
    drinks = DrinkItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = DrinkCategory
        fields = ['id', 'name', 'slug', 'description', 'order', 'is_active', 'drinks']


class SpecialMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecialMenu
        fields = '__all__'


class FullMenuSerializer(serializers.Serializer):
    """Serializer pour récupérer tout le menu en une fois"""
    food_categories = MenuCategorySerializer(many=True)
    drink_categories = DrinkCategorySerializer(many=True)
    special_menus = SpecialMenuSerializer(many=True)
