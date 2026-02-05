from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.MediaCategoryViewSet)
router.register(r'images', views.MediaImageViewSet)
router.register(r'carousel', views.CarouselSlideViewSet)
router.register(r'hero', views.HeroBannerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
