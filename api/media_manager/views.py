from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser
from .models import MediaCategory, MediaImage, CarouselSlide, HeroBanner
from .serializers import (
    MediaCategorySerializer, MediaImageSerializer,
    CarouselSlideSerializer, HeroBannerSerializer
)


class MediaCategoryViewSet(viewsets.ModelViewSet):
    queryset = MediaCategory.objects.all()
    serializer_class = MediaCategorySerializer
    lookup_field = 'slug'
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]


class MediaImageViewSet(viewsets.ModelViewSet):
    queryset = MediaImage.objects.all()
    serializer_class = MediaImageSerializer
    parser_classes = [MultiPartParser, FormParser]
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]
    
    def get_queryset(self):
        queryset = MediaImage.objects.all()
        
        # Filtre par catégorie
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        return queryset.select_related('category', 'uploaded_by')
    
    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)
    
    @action(detail=False, methods=['post'])
    def bulk_upload(self, request):
        """Upload multiple images at once"""
        files = request.FILES.getlist('files')
        category_id = request.data.get('category')
        
        created = []
        for f in files:
            image = MediaImage.objects.create(
                file=f,
                category_id=category_id if category_id else None,
                uploaded_by=request.user
            )
            created.append(MediaImageSerializer(image).data)
        
        return Response(created, status=status.HTTP_201_CREATED)


class CarouselSlideViewSet(viewsets.ModelViewSet):
    queryset = CarouselSlide.objects.all()
    serializer_class = CarouselSlideSerializer
    parser_classes = [MultiPartParser, FormParser]
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]
    
    def get_queryset(self):
        queryset = CarouselSlide.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)
        return queryset


class HeroBannerViewSet(viewsets.ModelViewSet):
    queryset = HeroBanner.objects.all()
    serializer_class = HeroBannerSerializer
    parser_classes = [MultiPartParser, FormParser]
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]
    
    def get_queryset(self):
        queryset = HeroBanner.objects.all()
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_active=True)
        return queryset
