from django.contrib import admin
from .models import Company, Contact, Email, Interaction, Phone, SocialMedia


class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "website")
    search_fields = ("name",)
    ordering = ("-created_at",)


admin.site.register(Company, CompanyAdmin)


class ContactAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "company", "status", "created_at")
    search_fields = ("first_name", "last_name", "company__name")
    list_filter = ("status", "company")
    ordering = ("-created_at",)


admin.site.register(Contact, ContactAdmin)


class EmailAdmin(admin.ModelAdmin):
    list_display = ("email", "contact", "created_at")
    search_fields = ("email", "contact__first_name", "contact__last_name")
    ordering = ("-created_at",)


admin.site.register(Email, EmailAdmin)


class PhoneAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "contact", "created_at")
    search_fields = ("phone_number", "contact__first_name", "contact__last_name")
    ordering = ("-created_at",)


admin.site.register(Phone, PhoneAdmin)


class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ("platform", "handle", "contact", "created_at")
    search_fields = ("platform", "handle", "contact__first_name", "contact__last_name")
    ordering = ("-created_at",)


admin.site.register(SocialMedia, SocialMediaAdmin)


class InteractionAdmin(admin.ModelAdmin):
    list_display = ("contact", "interaction_type",  "created_at")
    search_fields = ("contact__first_name", "contact__last_name")
    list_filter = ("interaction_type",)
    ordering = ("-created_at",)


admin.site.register(Interaction, InteractionAdmin)
