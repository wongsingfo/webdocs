from django.urls import path, include
from rest_framework.routers import DefaultRouter

from page import views

router = DefaultRouter()
router.register('documents', views.DocumentViewSet)
router.register('users', views.UserViewSet)
router.register('images', views.ImageViewSet)

urlpatterns = [
    path('', include(router.urls))
]
