from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'pages', views.PageViewSet)
router.register(r'sections', views.ContentSectionViewSet)
router.register(r'faq', views.FAQViewSet)

urlpatterns = [
    path('menu/', views.menu_pages, name='menu-pages'),
    path('', include(router.urls)),
]
