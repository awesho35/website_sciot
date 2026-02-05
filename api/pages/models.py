from django.db import models


class Page(models.Model):
    """Pages statiques du site"""
    title = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(unique=True)
    content = models.TextField(blank=True, verbose_name="Contenu")
    
    # SEO
    meta_title = models.CharField(max_length=200, blank=True, verbose_name="Meta Title")
    meta_description = models.TextField(blank=True, verbose_name="Meta Description")
    
    # Image de couverture
    cover_image = models.ImageField(upload_to='pages/', blank=True, null=True, verbose_name="Image de couverture")
    
    is_published = models.BooleanField(default=True, verbose_name="Publié")
    show_in_menu = models.BooleanField(default=False, verbose_name="Afficher dans le menu")
    menu_order = models.PositiveIntegerField(default=0, verbose_name="Ordre dans le menu")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Page"
        verbose_name_plural = "Pages"
        ordering = ['menu_order', 'title']
    
    def __str__(self):
        return self.title


class ContentSection(models.Model):
    """Sections de contenu réutilisables"""
    SECTION_TYPES = [
        ('text', 'Texte simple'),
        ('text_image', 'Texte + Image'),
        ('gallery', 'Galerie'),
        ('cta', 'Call to Action'),
        ('testimonial', 'Témoignage'),
        ('feature', 'Feature'),
    ]
    
    name = models.CharField(max_length=200, verbose_name="Nom interne")
    section_type = models.CharField(max_length=50, choices=SECTION_TYPES, default='text')
    
    title = models.CharField(max_length=200, blank=True, verbose_name="Titre")
    subtitle = models.CharField(max_length=300, blank=True, verbose_name="Sous-titre")
    content = models.TextField(blank=True, verbose_name="Contenu")
    
    # Image
    image = models.ImageField(upload_to='sections/', blank=True, null=True, verbose_name="Image")
    image_position = models.CharField(
        max_length=20, 
        choices=[('left', 'Gauche'), ('right', 'Droite')],
        default='right'
    )
    
    # CTA
    cta_text = models.CharField(max_length=100, blank=True, verbose_name="Texte du bouton")
    cta_url = models.URLField(blank=True, verbose_name="URL du bouton")
    
    # Style
    background_color = models.CharField(max_length=7, blank=True, verbose_name="Couleur de fond")
    text_color = models.CharField(max_length=7, blank=True, verbose_name="Couleur du texte")
    
    # Association aux pages
    page = models.ForeignKey(
        Page, 
        on_delete=models.CASCADE, 
        related_name='sections',
        null=True, 
        blank=True
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")
    
    class Meta:
        verbose_name = "Section de contenu"
        verbose_name_plural = "Sections de contenu"
        ordering = ['order']
    
    def __str__(self):
        return self.name


class FAQ(models.Model):
    """Questions fréquentes"""
    question = models.CharField(max_length=500, verbose_name="Question")
    answer = models.TextField(verbose_name="Réponse")
    category = models.CharField(max_length=100, blank=True, verbose_name="Catégorie")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")
    is_published = models.BooleanField(default=True, verbose_name="Publié")
    
    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ['category', 'order']
    
    def __str__(self):
        return self.question[:100]
