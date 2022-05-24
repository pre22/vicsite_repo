from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import TemplateView

from ..accounts.models import Balance, AmountInvested, DueDate, ProfilePic
from ..contents.models import HowToInvest, AboutUs, Our_offering, Carousel_Home, Who_we_are_sub
from ..investments.models import Package
from ..transactions.models import Deposit

TEMPLATE_URL = 'home'


def health_check(request):
    return JsonResponse({'status': 'ok'})

class HomepageView(TemplateView):
    template_name = 'front/homes.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        WHo_we_are_sub = Who_we_are_sub.objects.all()

        # context["carousel_home"] = Carousel_Home.objects.all()
        context.update({
            "package": Package.objects.all(),
            "HTI": HowToInvest.objects.all(),
            "aboutus": AboutUs.objects.all(),
            "our_offering": Our_offering.objects.all(),
            "who_we_are": WHo_we_are_sub,
            "carousel_home": Carousel_Home.objects.all(),
            # "blog": response,
        })
        return context


class ChartView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy("login")
    template_name = "charts.html"


class DashboardHomeView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy("login")
    template_name = "home/home.html"

    def get_context_data(self):
        context = super().get_context_data()
        context.update({
            "wallet_bal": Balance.objects.filter(user=self.request.user).first(),
            "amount_invested": AmountInvested.objects.filter(user=self.request.user).first(),
            "duedate": DueDate.objects.filter(user=self.request.user).first(),
            "deposit_h": Deposit.objects.filter(user=self.request.user),
            "pics": ProfilePic.objects.filter(user=self.request.user)
        })
        return context