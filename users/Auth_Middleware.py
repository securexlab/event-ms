from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout
import logging 

logger = logging.getLogger(__name__) 

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        unauthenticated_paths = [

        ]

        if request.path in unauthenticated_paths or request.path.startswith('/reset-password/') or request.path.startswith('/media/'):
            return self.get_response(request)

        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')

        if access_token:
            try:
                AccessToken(access_token)
                request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
            except TokenError:
                if refresh_token:
                    try:    
                        new_access_token = self.refresh_access_token(refresh_token)
                        request.META['HTTP_AUTHORIZATION'] = f'Bearer {new_access_token}'
                        response.set_cookie(
                            key="access_token",
                            value=new_access_token,
                            httponly=False,
                            secure=True,
                            samesite='Lax'
                        )
                        response = self.get_response(request)
                        return response
                    except TokenError:
                        logger.error("Refresh token invalid.")
                        response = self.handle_invalid_token(request)
                        return response
                else:
                    logger.error("No refresh token available.")
                    response = self.handle_invalid_token(request)
                    return response
        else:
            response = self.handle_invalid_token(request)
            return response

        response = self.get_response(request)
        return response

    def refresh_access_token(self, refresh_token):
        try:
            token = RefreshToken(refresh_token)
            return str(token.access_token)
        except TokenError:
            raise TokenError("Refresh token is invalid or expired.")

    def handle_invalid_token(self, request):
        messages.error(request, "Session expired. Please login again.")
        response = redirect('/')
        response.delete_cookie('refresh_token')
        response.delete_cookie('access_token')
        logout(request)
        return response