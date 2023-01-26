# views.py
from dj_rest_auth.views import UserDetailsView
from django.http import HttpResponseRedirect
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAdminUser
from .models import User
from .permissions import IsCreator, IsCreatorOrReadOnly
from .serializers import UserDetailSerializer, CustomUserDetailSerializer, UserImageSerializer

# Email Verification
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC

# Social Login
from dj_rest_auth.registration.views import SocialLoginView, SocialConnectView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

# Google
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter

# Kakao
from allauth.socialaccount.providers.kakao import views as kakao_view


# Custom User Detail
class CustomUserDetailsView(UserDetailsView):
    serializer_class = CustomUserDetailSerializer


# Confirm email
class ConfirmEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, *args, **kwargs):
        self.object = confirmation = self.get_object()
        email = confirmation.confirm(self.request)
        # A React Router Route will handle the failure scenario
        return HttpResponseRedirect(f'https://wafmate/fragment/emailauthenticate2301061457/{email}')

    def get_object(self, queryset=None):
        key = self.kwargs['key']
        email_confirmation = EmailConfirmationHMAC.from_key(key)
        if not email_confirmation:
            if queryset is None:
                queryset = self.get_queryset()
            try:
               email_confirmation = queryset.get(key=key.lower())
            except EmailConfirmation.DoesNotExist:
                # A React Router Route will handle the failure scenario
                return HttpResponseRedirect(f'https://wafmate/fragment/emailauthenticate2301061457/')
        return email_confirmation

    def get_queryset(self):
        qs = EmailConfirmation.objects.all_valid()
        qs = qs.select_related("email_address__user")
        return qs


# Social login
class GoogleLogin(SocialLoginView): # if you want to use Authorization Code Grant, use this
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client


class GoogleConnect(SocialConnectView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client


class KakaoLogin(SocialLoginView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    client_class = OAuth2Client


class KakaoConnect(SocialConnectView):
    adapter_class = kakao_view.KakaoOAuth2Adapter
    client_class = OAuth2Client


class UserDestroyView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsCreator | IsAdminUser]
    serializer_class = UserDetailSerializer


class UserImageRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsCreatorOrReadOnly | IsAdminUser]
    serializer_class = UserImageSerializer
