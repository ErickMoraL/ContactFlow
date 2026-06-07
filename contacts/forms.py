from django import forms
from .models import Company, Contact, Interaction, Email, Phone, SocialMedia


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
        self.fields["interaction_type"].widget.attrs.update(
            {
                "class": "select-primary",
                "placeholder": "Enter interaction type",
            }
        )
        self.fields["note"].widget.attrs.update(
            {
                "class": "textarea-primary",
                "placeholder": "Enter interaction note",
            }
        )
        self.fields["interaction_date"].widget.attrs.update(
            {
                "class": "input-primary",
                "placeholder": "Enter interaction date",
            }
        )

    class Meta:
        model = Interaction
        fields = [
            "interaction_type",
            "note",
            "interaction_date",
        ]


class CompanyForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    class Meta:
        model = Company
        fields = [
            "name",
            "industry",
            "website",
        ]

    def clean_name(self):
        name = self.cleaned_data["name"]

        if Company.objects.filter(user=self.user, name=name).exists():
            raise forms.ValidationError("You already have a company with this name.")

        return name


class EmailForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs.update(
            {
                "class": "input-primary",
                "placeholder": "Enter email",
            }
        )

    class Meta:
        model = Email
        fields = ["email"]


class PhoneForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields["phone_number"].widget.attrs.update(
            {
                "class": "input-primary",
                "placeholder": "Enter phone",
            }
        )

    class Meta:
        model = Phone
        fields = ["phone_number"]


class SocialMediaForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields["platform"].widget.attrs.update(
            {
                "class": "input-primary",
                "placeholder": "Twitter, Linkedin, Github",
            }
        )
        self.fields["url"].widget.attrs.update(
            {
                "class": "input-primary",
                "placeholder": "https://...",
            }
        )

    class Meta:
        model = SocialMedia
        fields = ["platform", "url"]
