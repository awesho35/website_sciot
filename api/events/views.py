from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Event, EventCategory
from .serializers import (
    EventListSerializer, EventDetailSerializer, 
    EventCategorySerializer, CalendarEventSerializer
)


class EventCategoryViewSet(viewsets.ModelViewSet):
    queryset = EventCategory.objects.all()
    serializer_class = EventCategorySerializer
    lookup_field = 'slug'
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        return [IsAdminUser()]


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    lookup_field = 'slug'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'status', 'is_featured', 'is_weekly_highlight']
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'week', 'upcoming', 'calendar']:
            return [AllowAny()]
        return [IsAdminUser()]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return EventListSerializer
        if self.action == 'calendar':
            return CalendarEventSerializer
        return EventDetailSerializer
    
    def get_queryset(self):
        queryset = Event.objects.all()
        
        # Pour les non-admins, ne montrer que les événements publiés
        if not self.request.user.is_staff:
            queryset = queryset.filter(status='published')
        
        # Filtres de date
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        month = self.request.query_params.get('month')
        year = self.request.query_params.get('year')
        
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)
        if month and year:
            queryset = queryset.filter(date__month=month, date__year=year)
        
        return queryset.order_by('date', 'start_time')
    
    @action(detail=False, methods=['get'])
    def week(self, request):
        """Événements de la semaine en cours"""
        events = Event.get_this_week_events()
        serializer = EventListSerializer(events, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Prochains événements"""
        limit = int(request.query_params.get('limit', 10))
        events = Event.get_upcoming_events(limit=limit)
        serializer = EventListSerializer(events, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def calendar(self, request):
        """Événements au format calendrier (FullCalendar)"""
        start = request.query_params.get('start')
        end = request.query_params.get('end')
        
        queryset = self.get_queryset()
        
        if start:
            queryset = queryset.filter(date__gte=start[:10])
        if end:
            queryset = queryset.filter(date__lte=end[:10])
        
        serializer = CalendarEventSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Statistiques des événements (admin)"""
        if not request.user.is_staff:
            return Response({'error': 'Non autorisé'}, status=403)
        
        today = timezone.now().date()
        this_month = today.replace(day=1)
        
        return Response({
            'total': Event.objects.count(),
            'published': Event.objects.filter(status='published').count(),
            'draft': Event.objects.filter(status='draft').count(),
            'upcoming': Event.objects.filter(date__gte=today, status='published').count(),
            'this_month': Event.objects.filter(date__gte=this_month, date__month=today.month).count(),
            'past': Event.objects.filter(date__lt=today).count(),
        })
