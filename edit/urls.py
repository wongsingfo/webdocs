from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:document_id>/', views.EditView.as_view(), name="edit"),
]
