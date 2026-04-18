from django.contrib import admin
from .models import Company, Contact, Email, Interaction, Phone, SocialMedia

# Register your models here.
admin.site.register(Company)
admin.site.register(Contact)
admin.site.register(Email)
admin.site.register(Interaction)
admin.site.register(Phone)
admin.site.register(SocialMedia)
