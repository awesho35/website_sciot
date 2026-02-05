from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from .models import MenuCategory, MenuItem, DrinkCategory, DrinkItem, SpecialMenu
from .serializers import (
    MenuCategorySerializer, MenuCategoryListSerializer, MenuItemSerializer,
    DrinkCategorySerializer, DrinkItemSerializer, SpecialMenuSerializer
)


@api_view(['GET'])
@permission_classes([AllowAny])
def full_menu(request):
    """Récupérer tout le menu en une seule requête"""
    food_categories = MenuCategory.objects.filter(is_active=True).prefetch_related('items')
    drink_categories = DrinkCategory.objects.filter(is_active=True).prefetch_related('drinks')
    special_menus = SpecialMenu.objects.filter(is_active=True)
    
    return Response({
        'food_categories': MenuCategorySerializer(food_categories, many=True).data,
        'drink_categories': DrinkCategorySerializer(drink_categories, many=True).data,
        'special_menus': SpecialMenuSerializer(special_menus, many=True).data,
    })


class MenuCategoryViewSet(viewsets.ModelViewSet):
    queryset = MenuCategory.objects.all()
    lookup_field = 'slug'
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return MenuCategoryListSerializer
        return MenuCategorySerializer
    
    def get_queryset(self):
        queryset = MenuCategory.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)
        return queryset.prefetch_related('items')


class MenuItemViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]
    
    def get_queryset(self):
        queryset = MenuItem.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_available=True, category__is_active=True)
        
        # Filtre par catégorie
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        return queryset.select_related('category')


class DrinkCategoryViewSet(viewsets.ModelViewSet):
    queryset = DrinkCategory.objects.all()
    serializer_class = DrinkCategorySerializer
    lookup_field = 'slug'
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]
    
    def get_queryset(self):
        queryset = DrinkCategory.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)
        return queryset.prefetch_related('drinks')


class DrinkItemViewSet(viewsets.ModelViewSet):
    queryset = DrinkItem.objects.all()
    serializer_class = DrinkItemSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]
    
    def get_queryset(self):
        queryset = DrinkItem.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_available=True, category__is_active=True)
        
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        return queryset.select_related('category')


class SpecialMenuViewSet(viewsets.ModelViewSet):
    queryset = SpecialMenu.objects.all()
    serializer_class = SpecialMenuSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]
    
    def get_queryset(self):
        queryset = SpecialMenu.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)
        return queryset
