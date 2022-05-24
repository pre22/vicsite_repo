from django.urls import path, include

from .views.auth import (
    Custom_PasswordResetView,
    Custom_PasswordResetDoneView,
    Custom_PasswordResetConfirmView,
    Custom_PasswordResetCompleteView,
    SignupView,
    CustomLoginView
)
from .views.profile import ProfileView, CustomPasswordChangeView, ProfileEdit

urlpatterns = [
    path('auth/', include([
        path("signup/", SignupView, name="signup"),
        path("login/", CustomLoginView.as_view(), name="login"),
    ])),
]

urlpatterns += [
    path('password_reset/', include([
        path("", Custom_PasswordResetView.as_view(), name="forgot_password"),
        path('done/', Custom_PasswordResetDoneView.as_view(), name='c_password_reset_done'),
        path('<uidb64>/<token>/', Custom_PasswordResetConfirmView.as_view(),
             name='c_password_reset_confirm'),
        path('complete/', Custom_PasswordResetCompleteView.as_view(), name='c_password_reset_complete'),
    ])),
]

urlpatterns += [
    path('profile/', include([
        path("", ProfileView.as_view(), name="profile"),
        path("password_change/", CustomPasswordChangeView.as_view(), name="password_change"),
        path("<int:pk>/edit/", ProfileEdit.as_view(), name="profile_edit"),
    ])),
]
