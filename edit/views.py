from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseBadRequest
from django.template import loader
from django.views import View

from .forms import DocumentForm, ImageForm
from .models import Document, Image


# Create your views here.

def index(request):
    latest_documents = Document.objects.order_by('-last_modified')[:5]
    template = loader.get_template('edit/index.html')
    context = {
        'latest_documents': latest_documents
    }
    output = template.render(context, request)
    # or shortcut reader(request, 'xxx.html', {context ...} )
    return HttpResponse(output)


class EditView(View):
    def get(self, request, document_id):
        document = get_object_or_404(Document, pk=document_id)
        return render(request, "edit/edit.html", {
            'document': document
        })

    # @login_required
    def post(self, request, document_id):
        # TODO: login
        #  https://docs.djangoproject.com/en/3.1/topics/auth/default/#how-to-log-a-user-in
        if not request.user.is_authenticated:
            return HttpResponse("Denied!")

        document = get_object_or_404(Document, pk=document_id)
        form = DocumentForm(request.POST)
        if form.is_valid():
            document.body = form.cleaned_data['body']
            document.save()
            return HttpResponseRedirect('/edit')
        else:
            return HttpResponseBadRequest("invalid data")


class ImageUploadView(View):

    def get(self, request, document_id):
        document = get_object_or_404(Document, pk=document_id)
        form = ImageForm(request.POST, request.FILES)
        return render(request, "edit/image.html", {
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
