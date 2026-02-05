from django.db import models


class MenuCategory(models.Model):
    """Catégories du menu (Entrées, Plats, Desserts, Boissons, etc.)"""
    name = models.CharField(max_length=100, verbose_name="Nom")
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, verbose_name="Description")
    icon = models.CharField(max_length=50, blank=True, verbose_name="Icône Bootstrap")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    
    class Meta:
        verbose_name = "Catégorie du menu"
        verbose_name_plural = "Catégories du menu"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class MenuItem(models.Model):
    """Items du menu"""
    category = models.ForeignKey(
        MenuCategory, 
        on_delete=models.CASCADE, 
        related_name='items',
        verbose_name="Catégorie"
    )
    name = models.CharField(max_length=200, verbose_name="Nom")
    description = models.TextField(blank=True, verbose_name="Description")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Prix (€)")
    
    # Options
    is_vegetarian = models.BooleanField(default=False, verbose_name="Végétarien")
    is_vegan = models.BooleanField(default=False, verbose_name="Végan")
    is_gluten_free = models.BooleanField(default=False, verbose_name="Sans gluten")
    is_spicy = models.BooleanField(default=False, verbose_name="Épicé")
    
    # Image
    image = models.ImageField(upload_to='menu/', blank=True, null=True, verbose_name="Image")
    
    # Disponibilité
    is_available = models.BooleanField(default=True, verbose_name="Disponible")
    is_featured = models.BooleanField(default=False, verbose_name="À la une")
    
    # Allergènes
    allergens = models.TextField(blank=True, verbose_name="Allergènes")
    
    # Ordre
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")
    
    # Meta
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Item du menu"
        verbose_name_plural = "Items du menu"
        ordering = ['category__order', 'order', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.price}€"


class DrinkCategory(models.Model):
    """Catégories de boissons (Vins, Bières, Cocktails, Softs, etc.)"""
    name = models.CharField(max_length=100, verbose_name="Nom")
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, verbose_name="Description")
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    
    class Meta:
        verbose_name = "Catégorie de boissons"
        verbose_name_plural = "Catégories de boissons"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name


class DrinkItem(models.Model):
    """Boissons"""
    VOLUME_CHOICES = [
        ('25cl', '25cl'),
        ('33cl', '33cl'),
        ('50cl', '50cl'),
        ('75cl', '75cl'),
        ('pint', 'Pinte'),
        ('half', 'Demi'),
        ('glass', 'Verre'),
        ('bottle', 'Bouteille'),
        ('shot', 'Shot'),
    ]
    
    category = models.ForeignKey(
        DrinkCategory, 
        on_delete=models.CASCADE, 
        related_name='drinks',
        verbose_name="Catégorie"
    )
    name = models.CharField(max_length=200, verbose_name="Nom")
    description = models.TextField(blank=True, verbose_name="Description")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Prix (€)")
    volume = models.CharField(max_length=20, choices=VOLUME_CHOICES, blank=True, verbose_name="Volume")
    
    # Pour les vins
    region = models.CharField(max_length=100, blank=True, verbose_name="Région")
    year = models.PositiveIntegerField(blank=True, null=True, verbose_name="Année")
    
    # Disponibilité
    is_available = models.BooleanField(default=True, verbose_name="Disponible")
    is_featured = models.BooleanField(default=False, verbose_name="À la une")
    
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")
    
    class Meta:
        verbose_name = "Boisson"
        verbose_name_plural = "Boissons"
        ordering = ['category__order', 'order', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.price}€"


class SpecialMenu(models.Model):
    """Menus spéciaux (Formule midi, Brunch, Menu enfant, etc.)"""
    name = models.CharField(max_length=200, verbose_name="Nom")
    description = models.TextField(verbose_name="Description")
    price = models.DecimalField(max_digits=6, decimal_places=2, verbose_name="Prix (€)")
    
    # Contenu
    content = models.TextField(verbose_name="Contenu du menu", help_text="Détail des plats inclus")
    
    # Disponibilité
    is_active = models.BooleanField(default=True, verbose_name="Actif")
    available_days = models.CharField(max_length=200, blank=True, verbose_name="Jours de disponibilité")
    available_hours = models.CharField(max_length=100, blank=True, verbose_name="Heures de disponibilité")
    
    # Image
    image = models.ImageField(upload_to='menu/special/', blank=True, null=True, verbose_name="Image")
    
    order = models.PositiveIntegerField(default=0, verbose_name="Ordre")
    
    class Meta:
        verbose_name = "Menu spécial"
        verbose_name_plural = "Menus spéciaux"
        ordering = ['order']
    
    def __str__(self):
        return f"{self.name} - {self.price}€"
