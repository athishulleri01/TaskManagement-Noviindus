import logging
from typing import Optional, Tuple
from django.conf import settings
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication, AuthUser
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import Token

# Configure logging
logger = logging.getLogger(__name__)

class CookieAuthentication(JWTAuthentication):
    """
    Custom authentication class to support JWT authentication via cookies.
    This class extends JWTAuthentication and checks for tokens in both
    the Authorization header and HTTP cookies.
    """

    def authenticate(self, request: Request) -> Optional[Tuple[AuthUser, Token]]:
        """
        Authenticate the request using JWT token.
        
        1. Checks for JWT token in the Authorization header.
        2. If not found, checks for JWT token in cookies.
        3. If a valid token is found, it retrieves and returns the authenticated user.
        
        :param request: The incoming HTTP request.
        :return: A tuple containing the authenticated user and token if authentication is successful, else None.
        """
        header = self.get_header(request)  # Extract JWT token from the Authorization header
        raw_token = None

        if header is not None:
            raw_token = self.get_raw_token(header)  # Extract the raw token from the header
        elif settings.COOKIE_NAME in request.COOKIES:
            raw_token = request.COOKIES.get(settings.COOKIE_NAME)  # Extract the token from cookies

        if raw_token is not None:
            try:
                validated_token = self.get_validated_token(raw_token)  # Validate the token
                return self.get_user(validated_token), validated_token  # Return the authenticated user

            except TokenError as e:
                logger.error(f"Token validation error: {str(e)}")  # Log any token validation errors
        
        return None  # Return None if authentication fails
