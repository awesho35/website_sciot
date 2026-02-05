from rest_framework import serializers
from .models import MediaCategory, MediaImage, CarouselSlide, HeroBanner


class MediaImageSerializer(serializers.ModelSerializer):
    url = serializers.ReadOnlyField()
    filename = serializers.ReadOnlyField()
    uploaded_by_name = serializers.CharField(source='uploaded_by.username', read_only=True)
    
    class Meta:
        model = MediaImage
        fields = [
            'id', 'title', 'file', 'url', 'filename', 'alt_text', 'category',
            'width', 'height', 'file_size', 'uploaded_at', 'uploaded_by', 'uploaded_by_name'
        ]
        read_only_fields = ['width', 'height', 'file_size', 'uploaded_at', 'uploaded_by']


class MediaCategorySerializer(serializers.ModelSerializer):
    images_count = serializers.SerializerMethodField()
    
    class Meta:
        model = MediaCategory
        fields = ['id', 'name', 'slug', 'description', 'images_count']
    
    def get_images_count(self, obj):
        return obj.images.count()


class CarouselSlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarouselSlide
        fields = '__all__'


class HeroBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeroBanner
        fields = '__all__'
