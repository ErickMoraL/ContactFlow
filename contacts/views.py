from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ContactForm, InteractionForm
from .models import Contact, Email, Phone, SocialMedia


def has_interaction_data(request):
    return any(
        request.POST.get(field, "").strip()
        for field in ["interaction_type", "interaction_date", "note"]
    )


def save_contact_emails(contact, emails):
    for email in emails:
        email = email.strip()

        if email:
            Email.objects.create(
                contact=contact,
                email=email,
            )


def save_contact_phones(contact, phones):
    for phone in phones:
        phone = phone.strip()

        if phone:
            Phone.objects.create(
                contact=contact,
                phone_number=phone,
            )


def save_contact_social_media(contact, platforms, urls):
    for platform, url in zip(platforms, urls):
        platform = platform.strip()
        url = url.strip()

        if platform and url:
            SocialMedia.objects.create(
                contact=contact,
                platform=platform,
                url=url,
            )


@login_required
def contact_list(request):
    query = request.GET.get("q", "")

    contacts = Contact.objects.prefetch_related("emails", "phones").filter(
        user=request.user
    )

    if query:
        contacts = contacts.filter(
            Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(company__name__icontains=query)
            | Q(status__icontains=query)
        )

    return render(request, "contacts/contact_list.html", {"contacts": contacts})


@login_required
def contact_detail(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)

    return render(request, "contacts/contact_detail.html", {"contact": contact})


@login_required
def contact_create(request):
    if request.method == "POST":
        form = ContactForm(request.POST, user=request.user)
        has_interaction = has_interaction_data(request)

        interaction_form = (
            InteractionForm(request.POST, user=request.user)
            if has_interaction
            else InteractionForm(user=request.user)
        )

        if form.is_valid() and (not has_interaction or interaction_form.is_valid()):
            with transaction.atomic():
                contact = form.save(commit=False)
                contact.user = request.user
                contact.save()

                save_contact_emails(
                    contact,
                    request.POST.getlist("emails"),
                )

                save_contact_phones(
                    contact,
                    request.POST.getlist("phones"),
                )

                save_contact_social_media(
                    contact,
                    request.POST.getlist("social_media_platforms"),
                    request.POST.getlist("social_media_urls"),
                )

                if has_interaction:
                    interaction = interaction_form.save(commit=False)
                    interaction.contact = contact
                    interaction.save()

            return redirect("contact_list")

    else:
        form = ContactForm(user=request.user)
        interaction_form = InteractionForm(user=request.user)
        has_interaction = False

    return render(
        request,
        "contacts/contact_create.html",
        {
            "form": form,
            "interaction_form": interaction_form,
            "has_interaction": has_interaction,
        },
    )


@login_required
def contact_edit(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)

    return render(request, "contacts/contact_edit.html", {"contact": contact})


@login_required
def contact_delete(request):
    return HttpResponse("Delete selected contacts")


@login_required
def contact_mark_closed(request):
    return HttpResponse("Mark selected contacts as closed")


@login_required
def contact_mark_lost(request):
    return HttpResponse("Mark selected contacts as lost")
