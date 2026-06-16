from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.urls import reverse

from .forms import ContactForm, InteractionForm, CompanyForm
from .formsSet import EmailFormSet, PhoneFormSet, SocialMediaFormSet, InteractionFormSet
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
    contact = get_object_or_404(
        Contact.objects.prefetch_related(
            "emails",
            "phones",
            "social_media",
            "interactions",
        ),
        pk=pk,
        user=request.user,
    )
    return render(
        request,
        "contacts/contact_detail.html",
        {
            "contact": contact,
            "cancel_url": reverse("contact_list"),
        },
    )


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
            messages.success(request, "Contact created successfully.")
            return redirect("contact_create")

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

    if request.method == "POST":
        contact_form = ContactForm(request.POST, user=request.user, instance=contact)
        email_formset = EmailFormSet(request.POST, instance=contact, prefix="emails")
        phone_formset = PhoneFormSet(request.POST, instance=contact, prefix="phones")
        socialmedia_formset = SocialMediaFormSet(
            request.POST, instance=contact, prefix="socials"
        )
        interction_formset = InteractionFormSet(
            request.POST, instance=contact, prefix="interactions"
        )

        if (
            contact_form.is_valid()
            and email_formset.is_valid()
            and phone_formset.is_valid()
            and socialmedia_formset.is_valid()
            and interction_formset.is_valid()
        ):
            contact_form.save()
            email_formset.save()
            phone_formset.save()
            socialmedia_formset.save()
            interction_formset.save()

            messages.success(request, "Contact updated successfully.")
            return redirect("contact_edit", pk=contact.pk)
    else:
        contact_form = ContactForm(instance=contact, user=request.user)
        email_formset = EmailFormSet(instance=contact, prefix="emails")
        phone_formset = PhoneFormSet(instance=contact, prefix="phones")
        socialmedia_formset = SocialMediaFormSet(instance=contact, prefix="socials")
        interction_formset = InteractionFormSet(instance=contact, prefix="interactions")

    return render(
        request,
        "contacts/contact_edit.html",
        {
            "contact_form": contact_form,
            "email_formset": email_formset,
            "phone_formset": phone_formset,
            "socialmedia_formset": socialmedia_formset,
            "interaction_formset": interction_formset,
        },
    )


@require_POST
@login_required
def contact_delete(request):
    selected_contact_ids = request.POST.getlist("selected_contacts")
    if not selected_contact_ids:
        messages.warning(request, "No contacts selected.")
        return redirect("contact_list")
    Contact.objects.filter(
        id__in=selected_contact_ids,
        user=request.user,
    ).delete()

    messages.success(request, "Contacts deleted successfully.")

    return redirect("contact_list")


@require_POST
@login_required
def contact_mark_closed(request):
    selected_contact_ids = request.POST.getlist("selected_contacts")
    if not selected_contact_ids:
        messages.warning(request, "no contacts selected.")
        return redirect("contact_list")
    Contact.objects.filter(
        id__in=selected_contact_ids,
        user=request.user,
    ).update(status=Contact.Status.CLOSED)
    messages.success(request, "Contacts marked as closed")
    return redirect("contact_list")


@require_POST
@login_required
def contact_mark_lost(request):
    selected_contact_ids = request.POST.getlist("selected_contacts")
    if not selected_contact_ids:
        messages.warning(request, "no contacts selected.")
        return redirect("contact_list")
    Contact.objects.filter(
        id__in=selected_contact_ids,
        user=request.user,
    ).update(status=Contact.Status.LOST)
    messages.success(request, "Contacts marked as lost")
    return redirect("contact_list")


@require_POST
@login_required
def contact_mark_negotiating(request):
    selected_contact_ids = request.POST.getlist("selected_contacts")
    if not selected_contact_ids:
        messages.warning(request, "no contacts selected.")
        return redirect("contact_list")
    Contact.objects.filter(
        id__in=selected_contact_ids,
        user=request.user,
    ).update(status=Contact.Status.NEGOTIATING)
    messages.success(request, "Contacts marked as negotiating")
    return redirect("contact_list")


@login_required
def create_company(request):
    if request.method == "POST":
        form = CompanyForm(request.POST, user=request.user)

        if form.is_valid():
            company = form.save(commit=False)
            company.user = request.user
            company.save()
            messages.success(request, "Company created successfully.")
            return redirect("create_company")
    else:
        form = CompanyForm(user=request.user)
    return render(request, "contacts/create_company.html", {"form": form})
