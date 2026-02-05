from django.db import models
from django.utils import timezone
from datetime import timedelta


class EventCategory(models.Model):
    """Catégories d'événements (Concert, DJ Set, Soirée thématique, etc.)"""
    name = models.CharField(max_length=100, verbose_name="Nom")
    slug = models.SlugField(unique=True)
    color = models.CharField(max_length=7, default="#1a1a2e", verbose_name="Couleur (hex)")
    icon = models.CharField(max_length=50, blank=True, verbose_name="Icône Bootstrap")
    description = models.TextField(blank=True, verbose_name="Description")
    
    class Meta:
        verbose_name = "Catégorie d'événement"
        verbose_name_plural = "Catégories d'événements"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Event(models.Model):
    """Événements/Concerts"""
    STATUS_CHOICES = [
        ('draft', 'Brouillon'),
        ('published', 'Publié'),
        ('cancelled', 'Annulé'),
        ('completed', 'Terminé'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(unique=True, blank=True)
    subtitle = models.CharField(max_length=300, blank=True, verbose_name="Sous-titre")
    description = models.TextField(blank=True, verbose_name="Description")
    short_description = models.CharField(max_length=200, blank=True, verbose_name="Description courte")
    
    # Dates
    date = models.DateField(verbose_name="Date")
    start_time = models.TimeField(verbose_name="Heure de début")
    end_time = models.TimeField(blank=True, null=True, verbose_name="Heure de fin")
    doors_open = models.TimeField(blank=True, null=True, verbose_name="Ouverture des portes")
    
    # Catégorie et image
    category = models.ForeignKey(
        EventCategory, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='events',
        verbose_name="Catégorie"
    )
    image = models.ImageField(upload_to='events/', blank=True, null=True, verbose_name="Image")
    thumbnail = models.ImageField(upload_to='events/thumbnails/', blank=True, null=True, verbose_name="Miniature")
    
    # Infos supplémentaires
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0, verbose_name="Prix (€)")
    is_free = models.BooleanField(default=True, verbose_name="Gratuit")
    ticket_url = models.URLField(blank=True, verbose_name="Lien billetterie")
    
    # Artiste
    artist_name = models.CharField(max_length=200, blank=True, verbose_name="Nom de l'artiste")
    artist_bio = models.TextField(blank=True, verbose_name="Bio de l'artiste")
    artist_website = models.URLField(blank=True, verbose_name="Site de l'artiste")
    artist_social = models.JSONField(default=dict, blank=True, verbose_name="Réseaux sociaux artiste")
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name="Statut")
    is_featured = models.BooleanField(default=False, verbose_name="À la une")
    is_weekly_highlight = models.BooleanField(default=False, verbose_name="Événement de la semaine")
    
    # Meta
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Événement"
        verbose_name_plural = "Événements"
        ordering = ['date', 'start_time']
    
    def __str__(self):
        return f"{self.title} - {self.date}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            base_slug = slugify(self.title)
            self.slug = f"{base_slug}-{self.date.strftime('%Y%m%d')}"
        super().save(*args, **kwargs)
    
    @property
    def is_past(self):
        return self.date < timezone.now().date()
    
    @property
    def is_today(self):
        return self.date == timezone.now().date()
    
    @property
    def is_upcoming(self):
        return self.date >= timezone.now().date()
    
    @property
    def formatted_date(self):
        """Date formatée en français"""
        days = ['LUN.', 'MAR.', 'MER.', 'JEU.', 'VEN.', 'SAM.', 'DIM.']
        months = ['JANV.', 'FÉVR.', 'MARS', 'AVR.', 'MAI', 'JUIN', 
                  'JUIL.', 'AOÛT', 'SEPT.', 'OCT.', 'NOV.', 'DÉC.']
        day_name = days[self.date.weekday()]
        day = self.date.day
        month = months[self.date.month - 1]
        return f"{day_name} {day} {month}"
    
    @classmethod
    def get_this_week_events(cls):
        """Récupérer les événements de la semaine"""
        today = timezone.now().date()
        end_of_week = today + timedelta(days=7)
        return cls.objects.filter(
            date__gte=today,
            date__lte=end_of_week,
            status='published'
        ).order_by('date', 'start_time')
    
    @classmethod
    def get_upcoming_events(cls, limit=10):
        """Récupérer les prochains événements"""
        today = timezone.now().date()
        return cls.objects.filter(
            date__gte=today,
            status='published'
        ).order_by('date', 'start_time')[:limit]
