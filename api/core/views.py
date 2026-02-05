from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from .models import SiteConfig, SocialLink, ContactMessage
from .serializers import SiteConfigSerializer, SocialLinkSerializer, ContactMessageSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def site_config(request):
    """Récupérer la configuration du site"""
    config = SiteConfig.objects.first()
    if not config:
        config = SiteConfig.objects.create()
    serializer = SiteConfigSerializer(config)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAdminUser])
def update_site_config(request):
    """Mettre à jour la configuration du site"""
    config = SiteConfig.objects.first()
    if not config:
        config = SiteConfig.objects.create()
    
    serializer = SiteConfigSerializer(config, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SocialLinkViewSet(viewsets.ModelViewSet):
    queryset = SocialLink.objects.all()
    serializer_class = SocialLinkSerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]


class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAdminUser()]
