from django.urls import path

from . import views

urlpatterns = [
    path("", views.contact_list, name="contact_list"),
    path("<int:pk>/", views.contact_detail, name="contact_detail"),
    path("create", views.contact_create, name="contact_create"),
    path("<int:pk>/edit", views.contact_edit, name="contact_edit"),
    path("delete_selected", views.contact_delete, name="contact_delete_selected"),
    path("mark_closed", views.contact_mark_closed, name="contact_mark_closed"),
    path("mark_lost", views.contact_mark_lost, name="contact_mark_lost"),
    path(
        "mark_negotiating",
        views.contact_mark_negotiating,
        name="contact_mark_negotiating",
    ),
    path("create_company", views.create_company, name="create_company"),
]
