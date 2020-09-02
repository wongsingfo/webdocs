from django.urls import path, include
from rest_framework.routers import DefaultRouter

from page import views

router = DefaultRouter()
router.register(r'documents', views.DocumentViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls))
]
