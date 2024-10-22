from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .Serializer import ResetPasswordRequestSerializer, ResetPassowrdSerializer
from .utils.EmailComponent import password_reset_email
from .models import PasswordReset, Profile
from .forms import ProfileForm


def login_page(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, "Invalid Username/Password")
            return redirect("/")
        else:
            login(request, user)
            token = RefreshToken.for_user(user)
            access_token = str(token.access_token)
            refresh_token = str(token)

            response = HttpResponseRedirect("/dashboard")
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=False,
                secure=True,
                samesite="Lax",
            )
            response.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=False,
                secure=True,
                samesite="Lax",
            )
            next_url = request.GET.get('next', '/dashboard') 
            return redirect(next_url)

    refresh_token = request.COOKIES.get("refresh_token")
    if refresh_token:
        try:
            RefreshToken(refresh_token)
            return redirect("/dashboard")
        except TokenError:
            logout(request)
    return render(request, "login.html")


class GetForgotPasswordForm(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        return render(request, "Form/Password-Reset-form.html")


User = get_user_model()

class RequestPasswordReset(APIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = User.objects.filter(email__iexact=email).first()

            if user:
                token_generator = PasswordResetTokenGenerator()
                token = token_generator.make_token(user)

                current_site = get_current_site(request).domain
                protocol = 'https' if request.is_secure() else 'http'
                reset_url = f"{protocol}://{current_site}/reset-password/{token}"

                reset = PasswordReset(email=email, token=token)
                reset.save()

                password_reset_email(reset_url, email)

                return Response(
                    {"success": "Email sent successfully"}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPassword(APIView):
    permission_classes = [AllowAny]
    serializer_class = ResetPassowrdSerializer

    def post(self, request, token):
        serlializer = self.serializer_class(data=request.data)
        if serlializer.is_valid():
            data = serlializer.validated_data
            new_password = data["new_password"]
            confirm_password = data["confirm_password"]

            if new_password != confirm_password:
                return Response({"error": "Passwords do not match"}, status=400)

            reset_obj = PasswordReset.objects.filter(token=token).first()

            if not reset_obj:
                return Response({"error": "Invalid token"}, status=400)

            user = User.objects.filter(email=reset_obj.email).first()

            if user:
                user.set_password(new_password)
                user.save()

                reset_obj.delete()

                return Response({"success": "Password updated"})
        else:
            return Response({"error": "No user found"}, status=404)

    def get(self, request, token):
        context = {"token": token}
        return render(request, "Form/Password-Change.html", context=context)


def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated!")
            return redirect("/")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, "Form/change-password-form.html", {"form": form})


class ProfileView(APIView):
    def get(self, request):
        profile = Profile.objects.first()
        if profile:
            form = ProfileForm(instance=profile)
        else:
            form = ProfileForm()

        return render(request, "Form/profile-form.html", {"form": form})

    def post(self, request):

        profile = Profile.objects.first()

        if profile:
            form = ProfileForm(request.POST, instance=profile)
        else:
            form = ProfileForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("api/dashboard/")

        return render(request, "Form/profile-form.html", {"form": form})
    
def custom_404_view(request, exception=None):
    return redirect(request,'/')

def self_logout(request):
    logout(request)
    response = redirect("/")
    response.delete_cookie("refresh_token")
    response.delete_cookie("access_token")
    return response
