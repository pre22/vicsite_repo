from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView

from ..accounts.models import Contact
from ..contents.models import Carousel_About, HowToInvest, AboutUs, Our_offering
from ..investments.models import Package


class AboutUsView(CreateView):
    model = Contact
    fields = "__all__"
    success_url = reverse_lazy("about_us")
    template_name = "front/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        carousel_about = Carousel_About.objects.all()
        context = {
            "package": Package.objects.all(),
            "how_to_invest": HowToInvest.objects.all(),
            "aboutus": AboutUs.objects.all(),
            "our_offering": Our_offering.objects.all(),
            "carousel_about": carousel_about,
            # "form": Contact.objects.all(),
        }
        return context
