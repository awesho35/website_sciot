from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.MenuCategoryViewSet)
router.register(r'items', views.MenuItemViewSet)
router.register(r'drinks/categories', views.DrinkCategoryViewSet)
router.register(r'drinks/items', views.DrinkItemViewSet)
router.register(r'special', views.SpecialMenuViewSet)

urlpatterns = [
    path('full/', views.full_menu, name='full-menu'),
    path('', include(router.urls)),
]
