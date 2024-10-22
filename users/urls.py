from django.urls import path
from .views import *
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.views import TokenBlacklistView

urlpatterns = [
    path("", login_page, name="login_page"),
    path("logout/", self_logout, name="logout"),
    path('reset-password-form/',GetForgotPasswordForm.as_view(), name='reset-password-form'),
    path("reset-password/", RequestPasswordReset.as_view(), name="reset-password"),
    path("reset-password/<str:token>/", ResetPassword.as_view(), name="reset-password"),
    path("change-password/", change_password, name="change_password"),
    path('get-profile-form/',ProfileView.as_view(),name="get-profile"),

    path("token", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
]
