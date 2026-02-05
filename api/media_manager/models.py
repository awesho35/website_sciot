from django.db import models
import os


def media_upload_path(instance, filename):
    """Générer le chemin d'upload basé sur la catégorie"""
    return f"gallery/{instance.category}/{filename}"


class MediaCategory(models.Model):
    """Catégories de médias pour organiser la galerie"""
    name = models.CharField(max_length=100, verbose_name="Nom")
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, verbose_name="Description")
    
    class Meta:
        verbose_name = "Catégorie média"
        verbose_name_plural = "Catégories médias"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class MediaImage(models.Model):
    """Images de la galerie"""
    title = models.CharField(max_length=200, blank=True, verbose_name="Titre")
    file = models.ImageField(upload_to='gallery/', verbose_name="Fichier")
    alt_text = models.CharField(max_length=300, blank=True, verbose_name="Texte alternatif")
    category = models.ForeignKey(
        MediaCategory, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='images',
        verbose_name="Catégorie"
    )
    
    # Métadonnées
    width = models.PositiveIntegerField(blank=True, null=True)
    height = models.PositiveIntegerField(blank=True, null=True)
    file_size = models.PositiveIntegerField(blank=True, null=True, verbose_name="Taille (bytes)")
    
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Date d'upload")
    uploaded_by = models.ForeignKey(
        'auth.User', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Uploadé par"
    )
    
    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return self.title or os.path.basename(self.file.name)
    
    def save(self, *args, **kwargs):
        # Auto-remplir le titre si vide
        if not self.title and self.file:
            self.title = os.path.splitext(os.path.basename(self.file.name))[0]
        
        # Récupérer les dimensions et taille
        if self.file:
            try:
                from PIL import Image
                img = Image.open(self.file)
                self.width, self.height = img.size
            except:
                pass
            
            try:
                self.file_size = self.file.size
            except:
                pass
        
        super().save(*args, **kwargs)
    
    @property
    def url(self):
        return self.file.url if self.file else None
    
    @property
    def filename(self):
        return os.path.basename(self.file.name) if self.file else None


class CarouselSlide(models.Model):
    """Slides du carrousel de la page d'accueil"""
    title = models.CharField(max_length=200, blank=True, verbose_name="Titre")
    subtitle = models.CharField(max_length=300, blank=True, verbose_name="Sous-titre")
    image = models.ImageField(upload_to='carousel/', verbose_name="Image")
    
    # Lien optionnel
    link_url = models.URLField(blank=True, verbose_name="URL du lien")
    link_text = models.CharField(max_length=100, blank=True, verbose_name="Texte du lien")
    
    # Ordre et activation
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    
    # Intervalle en millisecondes
    interval = models.PositiveIntegerField(default=5000, verbose_name="Intervalle (ms)")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Slide du carrousel"
        verbose_name_plural = "Slides du carrousel"
        ordering = ['order']
    
    def __str__(self):
        return self.title or f"Slide {self.order}"


class HeroBanner(models.Model):
    """Bannière hero de la page d'accueil"""
    title = models.CharField(max_length=200, verbose_name="Titre")
    subtitle = models.TextField(blank=True, verbose_name="Sous-titre")
    background_image = models.ImageField(upload_to='hero/', verbose_name="Image de fond")
    
    # CTA (Call to Action)
    cta_text = models.CharField(max_length=100, blank=True, verbose_name="Texte du bouton")
    cta_url = models.URLField(blank=True, verbose_name="URL du bouton")
    
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    
    class Meta:
        verbose_name = "Bannière Hero"
        verbose_name_plural = "Bannières Hero"
    
    def __str__(self):
        return self.title
