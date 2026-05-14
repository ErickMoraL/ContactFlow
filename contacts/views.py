from django.shortcuts import render, redirect

from django.http import HttpResponse
from .models import Contact
from django.db.models import Q
from .forms import ContactForm
from django.contrib.auth.decorators import login_required


@login_required
def contact_list(request):

    query = request.GET.get("q", "")

    contacts = Contact.objects.prefetch_related("emails", "phones").all()

    if query:
        contacts = contacts.filter(
            Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(company__name__icontains=query)
            | Q(status__icontains=query)
        )

    return render(request, "contact_list.html", {"contacts": contacts})


@login_required
def contact_detail(request, pk):
    contact = Contact.objects.get(pk=pk)

    return render(request, "contact_detail.html", {"contact": contact})


@login_required
def contact_create(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("contact_list")
    else:
        form = ContactForm()

    return render(request, "contact_create.html", {"form": form})

@login_required
def contact_edit(request, pk):
    contact = Contact.objects.get(pk=pk)

    return render(request, "contact_edit.html", {"contact": contact})

@login_required
def contact_delete(request):
    return HttpResponse("Delete selected contacts")

@login_required
def contact_mark_closed(request):
    return HttpResponse("Mark selected contacts as closed")


@login_required
def contact_mark_lost(request):
    return HttpResponse("Mark selected contacts as lost")
