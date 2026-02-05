from django.db import models


class SiteConfig(models.Model):
    """Configuration générale du site"""
    site_name = models.CharField(max_length=200, default="Le Sciøt Cial Club", verbose_name="Nom du site")
    tagline = models.CharField(max_length=500, blank=True, verbose_name="Slogan")
    description = models.TextField(blank=True, verbose_name="Description")
    
    # Contact
    phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    email = models.EmailField(blank=True, verbose_name="Email")
    
    # Adresse
    address_line1 = models.CharField(max_length=200, blank=True, verbose_name="Adresse ligne 1")
    address_line2 = models.CharField(max_length=200, blank=True, verbose_name="Adresse ligne 2")
    city = models.CharField(max_length=100, blank=True, verbose_name="Ville")
    postal_code = models.CharField(max_length=10, blank=True, verbose_name="Code postal")
    region = models.CharField(max_length=100, blank=True, verbose_name="Région")
    
    # Google Maps
    google_maps_embed_url = models.URLField(blank=True, verbose_name="URL Google Maps Embed")
    google_maps_directions_url = models.URLField(blank=True, verbose_name="URL Google Maps Directions")
    
    # Logo et favicon
    logo = models.ImageField(upload_to='site/', blank=True, null=True, verbose_name="Logo")
    favicon = models.ImageField(upload_to='site/', blank=True, null=True, verbose_name="Favicon")
    
    # Horaires d'ouverture
    opening_hours = models.TextField(blank=True, verbose_name="Horaires d'ouverture")
    
    # Meta
    meta_title = models.CharField(max_length=200, blank=True, verbose_name="Meta Title")
    meta_description = models.TextField(blank=True, verbose_name="Meta Description")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Configuration du site"
        verbose_name_plural = "Configuration du site"
    
    def __str__(self):
        return self.site_name
    
    def save(self, *args, **kwargs):
        # S'assurer qu'il n'y a qu'une seule configuration
        if not self.pk and SiteConfig.objects.exists():
            raise ValueError("Il ne peut y avoir qu'une seule configuration de site")
        super().save(*args, **kwargs)


class SocialLink(models.Model):
    """Liens vers les réseaux sociaux"""
    PLATFORMS = [
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('youtube', 'YouTube'),
        ('twitter', 'Twitter/X'),
        ('tiktok', 'TikTok'),
        ('spotify', 'Spotify'),
        ('soundcloud', 'SoundCloud'),
    ]
    
    ICONS = {
        'instagram': 'bi-instagram',
        'facebook': 'bi-facebook',
        'youtube': 'bi-youtube',
        'twitter': 'bi-twitter-x',
        'tiktok': 'bi-tiktok',
        'spotify': 'bi-spotify',
        'soundcloud': 'bi-soundcloud',
    }
    
    platform = models.CharField(max_length=50, choices=PLATFORMS, verbose_name="Plateforme")
    url = models.URLField(verbose_name="URL")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")
    
    class Meta:
        verbose_name = "Réseau social"
        verbose_name_plural = "Réseaux sociaux"
        ordering = ['order']
    
    def __str__(self):
        return f"{self.get_platform_display()} - {self.url}"
    
    @property
    def icon(self):
        return self.ICONS.get(self.platform, 'bi-link')


class ContactMessage(models.Model):
    """Messages de contact"""
    name = models.CharField(max_length=200, verbose_name="Nom")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")
    subject = models.CharField(max_length=300, verbose_name="Sujet")
    message = models.TextField(verbose_name="Message")
    
    is_read = models.BooleanField(default=False, verbose_name="Lu")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date d'envoi")
    
    class Meta:
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
