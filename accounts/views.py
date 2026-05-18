from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordChangeView,
    PasswordResetCompleteView,
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .forms import RegisterForm
from .forms import UserProfileForm
from django.contrib.auth.models import User


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("contact_list")
    else:
        form = RegisterForm()

    return render(request, "accounts/register.html", {"form": form})


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    pass


class CustomPasswordChangeView(PasswordChangeView):
    template_name = "accounts/password_change_form.html"
    success_url = reverse_lazy("password_change_done")


class CustomPasswordResetView(PasswordResetView):
    template_name = "accounts/password_reset_form.html"
    success_url = reverse_lazy("password_reset_done")


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "accounts/password_reset_done.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "accounts/password_reset_confirm.html"
    success_url = reverse_lazy("password_reset_complete")


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "accounts/password_reset_complete.html"


@login_required
def profile(request):
    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, "accounts/profile.html", {"form": form})
