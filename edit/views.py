from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
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


def edit(request, document_id):

    # or shortcut: get_object_or_404(Document, pk=document_id)
    try:
        document = Document.objects.get(pk=document_id)
    except Document.DoesNotExist:
        raise Http404("Document %s does not exist" % document_id)

    if request.method == "POST":
        # TODO: login
        #  https://docs.djangoproject.com/en/3.1/topics/auth/default/#how-to-log-a-user-in
        if not request.user.is_authenticated:
            return HttpResponse("Denied!")
        try:
            document.body = request.POST['body']
            document.save()
        except KeyError:
            return HttpResponse("POST failed")
        else:
            return HttpResponseRedirect('/edit')
    else:
        return render(request, "edit/edit.html", {
            'document': document
        })
