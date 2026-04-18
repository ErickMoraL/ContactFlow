from django.db import models
from django.conf import settings


class Company(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=150)
    industry = models.CharField(max_length=100, blank=True)
    website = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Contact(models.Model):
    class Status(models.TextChoices):
        NEW = "new", "nuevo"
        INTERESTED = "interested", "interesado"
        NEGOTIATING = "negotiating", "negociando"
        CLOSED = "closed", "cerrado"
        LOST = "lost", "perdido"

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="contacts",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or "Unnamed Contact"


class Email(models.Model):
    contact = models.ForeignKey(
        Contact, on_delete=models.CASCADE, related_name="emails"
    )
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Phone(models.Model):
    contact = models.ForeignKey(
        Contact, on_delete=models.CASCADE, related_name="phones"
    )
    phone_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone_number


class SocialMedia(models.Model):
    contact = models.ForeignKey(
        Contact, on_delete=models.CASCADE, related_name="social_media"
    )
    platform = models.CharField(max_length=50)
    handle = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.platform}: {self.handle}"


class Interaction(models.Model):
    class InteractionType(models.TextChoices):
        CALL = "call", "llamada"
        MESSAGE = "message", "mensaje"
        MEETING = "meeting", "reunión"
        EMAIL = "email", "correo electrónico"

    contact = models.ForeignKey(
        Contact, on_delete=models.CASCADE, related_name="interactions"
    )
    interaction_type = models.CharField(max_length=20, choices=InteractionType.choices)
    note = models.TextField()
    interaction_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_interaction_type_display()} - {self.contact} - {self.interaction_date.strftime('%Y-%m-%d %H:%M')}"  # type: ignore[attr-defined]
