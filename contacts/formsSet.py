from django.forms import inlineformset_factory
from .models import Contact, Phone, Email, Interaction, SocialMedia
from .forms import EmailForm, InteractionForm, PhoneForm, SocialMediaForm

EmailFormSet = inlineformset_factory(
    Contact, Email, form=EmailForm, extra=1, can_delete=True
)

PhoneFormSet = inlineformset_factory(
    Contact, Phone, form=PhoneForm, extra=1, can_delete=True
)

SocialMediaFormSet = inlineformset_factory(
    Contact, SocialMedia, form=SocialMediaForm, extra=1, can_delete=True
)

InteractionFormSet = inlineformset_factory(
    Contact, Interaction, form=InteractionForm, extra=1, can_delete=True
)
