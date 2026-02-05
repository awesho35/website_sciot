from rest_framework import serializers
from .models import SiteConfig, SocialLink, ContactMessage


class SocialLinkSerializer(serializers.ModelSerializer):
    icon = serializers.ReadOnlyField()
    
    class Meta:
        model = SocialLink
        fields = ['id', 'platform', 'url', 'icon', 'is_active', 'order']


class SiteConfigSerializer(serializers.ModelSerializer):
    social_links = serializers.SerializerMethodField()
    
    class Meta:
        model = SiteConfig
        fields = '__all__'
    
    def get_social_links(self, obj):
        links = SocialLink.objects.filter(is_active=True)
        return SocialLinkSerializer(links, many=True).data


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'phone', 'subject', 'message', 'created_at']
        read_only_fields = ['created_at']
