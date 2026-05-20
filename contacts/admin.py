from django.contrib import admin
from .models import Company, Contact, Email, Interaction, Phone, SocialMedia


class EmailInline(admin.TabularInline):
    model = Email
    extra = 1


class PhoneInline(admin.TabularInline):
    model = Phone
    extra = 1


class SocialMediaInline(admin.TabularInline):
    model = SocialMedia
    extra = 1


class InteractionInline(admin.TabularInline):
    model = Interaction
    extra = 1


class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "website")
    search_fields = ("name",)
    ordering = ("-created_at",)


admin.site.register(Company, CompanyAdmin)


class ContactAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "company",
        "status",
        "admin_primary_email",
        "admin_primary_phone",
        "created_at",
    )

    @admin.display(description="Email")
    def admin_primary_email(self, obj):
        return obj.primary_email

    @admin.display(description="Phone")
    def admin_primary_phone(self, obj):
        return obj.primary_phone

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("company")
            .prefetch_related("emails", "phones")
        )

    search_fields = (
        "first_name",
        "last_name",
        "company__name",
        "emails__email",
        "phones__phone_number",
    )

    list_filter = ("status", "company")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"

    inlines = [
        EmailInline,
        PhoneInline,
        SocialMediaInline,
        InteractionInline,
    ]


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
    list_display = ("platform", "url", "contact", "created_at")
    search_fields = ("platform", "url", "contact__first_name", "contact__last_name")
    ordering = ("-created_at",)


admin.site.register(SocialMedia, SocialMediaAdmin)


class InteractionAdmin(admin.ModelAdmin):
    list_display = ("contact", "interaction_type", "created_at")
    search_fields = ("contact__first_name", "contact__last_name")
    list_filter = ("interaction_type",)
    ordering = ("-created_at",)


admin.site.register(Interaction, InteractionAdmin)
