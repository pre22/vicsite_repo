from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.http import request, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, CreateView, UpdateView
from ..models import Balance, ProfilePic

User = get_user_model()

class ProfileView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('login')
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = {
            "bal": Balance.user,
            "pics": ProfilePic.user,
        }
        return context


class ProfileEdit(LoginRequiredMixin, UpdateView):
    model = User
    fields = (
        "firstname",
        "lastname",
        "occupation",
        "email",
        "phone",
        "sex",
    )
    success_url = reverse_lazy("profile")
    template_name = "accounts/profile_edit.html"


class ProfilePicsView(LoginRequiredMixin, UpdateView):
    model = ProfilePic
    fields = {"img", }
    template_name = "accounts/profile_edit.html"
    context_object_name = "pics"
    success_url = reverse_lazy("profile")


class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = "accounts/change_password.html"
    success_url = reverse_lazy("profile")

# def ProfileEdit(request, id):
#     data = get_object_or_404(CustomUser, id=id)
#     form = ProfileUpdateForm(instance=data)

#     if request.method == "POST":
#         message = "Your Profile has been successfully updated!"
#         form = ProfileUpdateForm(request.POST, instance=data)

#         if form.is_valid():
#             form.save(request)
#             messages.success(request, message)
#             return reverse_lazy("profile")
#     else:
#         form = ProfileUpdateForm(instance=data)
#     return render(request, "accounts/profile_edit.html", {"form": form})

# def ProfilePicsView(request, id):
#     data = get_object_or_404(Profilepic, id=id)
#     form = Profilepic(instance=data)

#     if request.method == "POST":
#         form = ProfilePicForm(request.POST, instance=pic)

#         if form.is_valid():
#             form.save(request)
#             return reverse_lazy("profile")
#     else:
#         form = ProfilePicForm(instance=data)
#     return render(request, "accounts/profile_edit.html", {"pics": form})



