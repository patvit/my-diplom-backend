#from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from .models import Document

def redirect_to_document(request, hash):
    try:
       document = get_object_or_404(Document, share_link=f'http://127.0.0.1:8000/s/{hash}')
       file_path = document.file.path
       with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{document.filename}"'
            response['Content-Length'] = document.file.size
            return response
    except Document.DoesNotExist:
        return HttpResponse("Share link not found", status=404)