from django import forms
from .models import Company, Contact, Interaction


class ContactForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        companies = Company.objects.none()
        if user is not None and user.is_authenticated:
            companies = Company.objects.filter(user=user).order_by("name")

        self.fields["company"].queryset = companies

    class Meta:
        model = Contact
        fields = [
            "first_name",
            "last_name",
            "status",
            "company",
        ]


class InteractionForm(forms.ModelForm):
    interaction_date = forms.DateTimeField(
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(
            attrs={"type": "datetime-local"},
            format="%Y-%m-%dT%H:%M",
        ),
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Interaction
        fields = [
            "interaction_type",
            "note",
            "interaction_date",
        ]
