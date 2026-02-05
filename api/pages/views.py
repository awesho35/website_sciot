from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from .models import Page, ContentSection, FAQ
from .serializers import (
    PageListSerializer, PageDetailSerializer,
    ContentSectionSerializer, FAQSerializer
)


class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    lookup_field = 'slug'
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PageListSerializer
        return PageDetailSerializer
    
    def get_queryset(self):
        queryset = Page.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_published=True)
        return queryset.prefetch_related('sections')


class ContentSectionViewSet(viewsets.ModelViewSet):
    queryset = ContentSection.objects.all()
    serializer_class = ContentSectionSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]


class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]
    
    def get_queryset(self):
        queryset = FAQ.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_published=True)
        
        # Filtre par catégorie
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        return queryset


@api_view(['GET'])
@permission_classes([AllowAny])
def menu_pages(request):
    """Récupérer les pages à afficher dans le menu"""
    pages = Page.objects.filter(is_published=True, show_in_menu=True).order_by('menu_order')
    serializer = PageListSerializer(pages, many=True)
    return Response(serializer.data)
