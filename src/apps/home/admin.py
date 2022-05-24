from django.contrib import admin

# Register your models here.
from django.contrib.redirects.admin import RedirectAdmin as BaseRedirectAdmin
from django.contrib.redirects.models import Redirect as BaseRedirect

admin.site.unregister(BaseRedirect)

@admin.register(BaseRedirect)
class RedirectAdmin(BaseRedirectAdmin):
    def get_list_display(self, request):
        return super().get_list_display(request) + ('site',)