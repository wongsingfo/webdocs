from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseBadRequest
from django.views import View
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

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
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ['title', 'owner__username']
    search_fields = ['=id', '^title', '^owner__username']
    ordering_fields = ['id', 'owner', 'created', 'last_modified']


    # overrides method of class CreateModelMixin.
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
