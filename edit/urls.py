from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:document_id>/', views.edit, name="edit"),
]
