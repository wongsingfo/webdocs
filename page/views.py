from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseBadRequest
from django.views import View
from rest_framework import viewsets, permissions

from .forms import DocumentForm, ImageForm
from .models import Document, Image


# Create your views here.
from .permissions import IsOwnerOrReadOnly
from .serializers import UserSerializer, DocumentSerializer, ImageSerializer


class ImageUploadView(View):

    def get(self, request, document_id):
        document = get_object_or_404(Document, pk=document_id)
        form = ImageForm(request.POST, request.FILES)
        return render(request, "page/image.html", {
            "form": form,
            "document": document,
        })

    def post(self, request, document_id):
        document = get_object_or_404(Document, pk=document_id)
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = Image(document=document, image=form.cleaned_data['image'])
            image.save()
            return HttpResponse(image.image.url)
        else:
            return HttpResponseBadRequest("invalid data")


class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]

    # overrides method of class CreateModelMixin.
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
