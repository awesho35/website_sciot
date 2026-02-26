from rest_framework import serializers
from .models import Event, EventCategory


class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = EventCategory
        fields = ['id', 'name', 'slug', 'color', 'icon', 'description']


class EventListSerializer(serializers.ModelSerializer):
    """Serializer pour les listes d'événements"""
    category = EventCategorySerializer(read_only=True)
    formatted_date = serializers.ReadOnlyField()
    is_past = serializers.ReadOnlyField()
    is_upcoming = serializers.ReadOnlyField()
    
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'slug', 'subtitle', 'short_description', 'date', 'start_time',
            'end_time', 'doors_open', 'category', 'image', 'thumbnail',
            'price', 'is_free', 'ticket_url', 'artist_name',
            'is_featured', 'is_weekly_highlight',
            'formatted_date', 'is_past', 'is_upcoming', 'status'
        ]


class EventDetailSerializer(serializers.ModelSerializer):
    """Serializer pour le détail d'un événement"""
    category = EventCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=EventCategory.objects.all(),
        source='category',
        write_only=True,
        required=False
    )
    formatted_date = serializers.ReadOnlyField()
    is_past = serializers.ReadOnlyField()
    is_today = serializers.ReadOnlyField()
    is_upcoming = serializers.ReadOnlyField()
    
    class Meta:
        model = Event
        fields = '__all__'


class CalendarEventSerializer(serializers.ModelSerializer):
    """Serializer pour le calendrier (FullCalendar)"""
    start = serializers.SerializerMethodField()
    end = serializers.SerializerMethodField()
    color = serializers.CharField(source='category.color', read_only=True)
    
    class Meta:
        model = Event
        fields = ['id', 'title', 'start', 'end', 'color', 'status']
    
    def get_start(self, obj):
        from datetime import datetime
        return datetime.combine(obj.date, obj.start_time).isoformat()
    
    def get_end(self, obj):
        from datetime import datetime
        if obj.end_time:
            return datetime.combine(obj.date, obj.end_time).isoformat()
        return None
