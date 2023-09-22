from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ProductViewSet, LessonViewSet

router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('lessons', LessonViewSet, basename='lessons')

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls))
]
