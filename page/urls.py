from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:document_id>/', views.EditView.as_view(), name="page"),
    path('<int:document_id>/image', views.ImageUploadView.as_view(), name="upload_image")
]
