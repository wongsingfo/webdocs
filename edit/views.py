from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader
from .models import Document


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


def markdown_edit(request, document_id):
    # or shortcut: get_object_or_404(Document, pk=document_id)
    try:
        document = Document.objects.get(pk=document_id)
    except Document.DoesNotExist:
        raise Http404("Document %s does not exist" % document_id)

    return render(request, "edit/markdown_edit.html", {
        'document': document
    })
