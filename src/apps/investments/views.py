from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .models import Investment, Package


class InvestView(LoginRequiredMixin, CreateView):
    """
    This class displays the investment form
    """
    login_url = reverse_lazy("login")
    model = Investment
    template_name = "investments/invest.html"
    fields = ["package", "amount",]
    success_url = reverse_lazy("transactions")
    # context_object_name = "form"
 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["package"] = Package.objects.all()
        
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
