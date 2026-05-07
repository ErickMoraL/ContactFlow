from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Contact


def contact_list(request):
    contacts = Contact.objects.all()
    return render(request, "contact_list.html", {"contacts": contacts})
