from django.urls import path, include

from .home.views import DashboardHomeView, ChartView, HomepageView

urlpatterns = [
    path('home/', include('apps.home.urls')),
    path('pages/', include('apps.pages.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('investments/', include('apps.investments.urls')),
    path('transactions/', include('apps.transactions.urls')),
]

urlpatterns += [
    path('dashboard/', include([
        path("", DashboardHomeView.as_view(), name="home"),
        path("charts/", ChartView.as_view(), name="charts"),
    ]))
]

urlpatterns += [
    path("", HomepageView.as_view(), name="homepage"),
]
