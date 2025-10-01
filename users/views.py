import logging
from typing import Optional
from django.conf import settings
from djoser.social.views import ProviderAuthView
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

logger = logging.getLogger(__name__)


def set_auth_cookies(
    response: Response, access_token: str, refresh_token: Optional[str] = None
) -> None:
    """
    Sets authentication cookies for access and refresh tokens.
    
    Args:
        response (Response): The HTTP response object.
        access_token (str): The access token to be set in the cookies.
        refresh_token (Optional[str]): The refresh token to be set in the cookies (optional).
    """
    access_token_lifetime = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()
    
    # Common cookie settings
    cookie_settings = {
        "path": settings.COOKIE_PATH,
        "secure": settings.COOKIE_SECURE,
        "httponly": settings.COOKIE_HTTPONLY,
        "samesite": settings.COOKIE_SAMESITE,
        "max_age": access_token_lifetime,
    }
    
    # Set access token in cookies
    response.set_cookie("access", access_token, **cookie_settings)

    if refresh_token:
        refresh_token_lifetime = settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()
        refresh_cookie_settings = cookie_settings.copy()
        refresh_cookie_settings["max_age"] = refresh_token_lifetime
        response.set_cookie("refresh", refresh_token, **refresh_cookie_settings)

    # Set logged_in cookie (not httponly, used for frontend checks)
    logged_in_cookie_settings = cookie_settings.copy()
    logged_in_cookie_settings["httponly"] = False
    response.set_cookie("logged_in", "true", **logged_in_cookie_settings)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom authentication view for obtaining access and refresh tokens.
    Sets the tokens in cookies instead of returning them in the response body.
    """
    def post(self, request: Request, *args, **kwargs) -> Response:
        token_res = super().post(request, *args, **kwargs)

        if token_res.status_code == status.HTTP_200_OK:
            access_token = token_res.data.get("access")
            refresh_token = token_res.data.get("refresh")

            if access_token and refresh_token:
                set_auth_cookies(token_res, access_token, refresh_token)
                token_res.data.pop("access", None)
                token_res.data.pop("refresh", None)
                token_res.data["message"] = "Login Successful."
            else:
                token_res.data["message"] = "Login Failed"
                logger.error("Access or refresh token missing in login response.")

        return token_res


class CustomTokenRefreshView(TokenRefreshView):
    """
    Custom authentication view for refreshing the access token.
    Uses the refresh token from cookies if it's not in the request body.
    """
    def post(self, request: Request, *args, **kwargs) -> Response:
        refresh_token = request.COOKIES.get("refresh")

        if refresh_token:
            request.data["refresh"] = refresh_token

        refresh_res = super().post(request, *args, **kwargs)

        if refresh_res.status_code == status.HTTP_200_OK:
            access_token = refresh_res.data.get("access")
            refresh_token = refresh_res.data.get("refresh")

            if access_token and refresh_token:
                set_auth_cookies(refresh_res, access_token, refresh_token)
                refresh_res.data.pop("access", None)
                refresh_res.data.pop("refresh", None)
                refresh_res.data["message"] = "Access tokens refreshed successfully"
            else:
                refresh_res.data["message"] = "Token refresh failed."
                logger.error("Access or refresh token missing in refresh response.")

        return refresh_res



class LogoutAPIView(APIView):
    """
    API view to log out a user by clearing authentication cookies.
    """
    def post(self, request: Request, *args, **kwargs) -> Response:
        response = Response({"message": "Logged out successfully."}, status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        response.delete_cookie("logged_in")
        return response
