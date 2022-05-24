from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView, \
    PasswordResetDoneView, LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy

from ..forms.custom import CustomSignupForm, CustomLoginForm


class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = "registration/login.html"
    success_url = reverse_lazy("home")


def SignupView(request):
    if request.method == "POST":
        form = CustomSignupForm(request.POST)

        if form.is_valid():
            form.save(request)
            return HttpResponseRedirect(reverse_lazy("login"))
    else:
        form = CustomSignupForm()
    return render(request, "registration/register.html", {"form": form})

class Custom_PasswordResetView(PasswordResetView):
    template_name = "password/forgot_password.html"
    subject_template_name = 'password/password_reset_subject.html'
    email_template_name = 'password/password_reset_email.html'
    success_url = reverse_lazy("c_password_reset_done")

class Custom_PasswordResetDoneView(PasswordResetDoneView):
    template_name = "password/password_reset_done.html"
    success_url = reverse_lazy("c_password_reset_confirm")

class Custom_PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "password/password_reset_confirm.html"
    success_url = reverse_lazy("c_password_reset_complete")

class Custom_PasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "password/password_reset_complete.html"