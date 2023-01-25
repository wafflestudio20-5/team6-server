from django.contrib.auth import authenticate
from rest_framework import serializers
from dj_rest_auth.serializers import LoginSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from .models import User

from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from allauth.account import app_settings
from allauth.account.adapter import get_adapter
from allauth.account.utils import user_pk_to_url_str, user_username, filter_users_by_email
from allauth.utils import build_absolute_uri
from dj_rest_auth.forms import AllAuthPasswordResetForm
from dj_rest_auth.serializers import PasswordResetSerializer


class CustomRegisterSerializer(RegisterSerializer):
    username = None

    def get_cleaned_data(self):
        return {
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
        }


class CustomLoginSerializer(LoginSerializer):
    username = None

    def authenticate(self, **options):
        return authenticate(self.context["request"], **options)

    def validate(self, attrs):
        username = None
        email = attrs.get("email")
        password = attrs.get("password")
        if email and password:
            user = self.get_auth_user(username, email, password)
            if not user:
                msg = "Unable to log in with provided credentials."
                raise serializers.ValidationError({'Authorization error': msg}, code="authorization")
        self.validate_email_verification_status(user)
        attrs["user"] = user

        return attrs


class UserDetailSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if "localhost" in ret["image"]:
            ret["image"] = ret["image"].replace("localhost", "3.38.100.94")
        return ret

    class Meta:
        model = User
        fields = ['id', 'email', 'nickname', 'detail', 'image']


class CustomUserDetailSerializer(UserDetailSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if "localhost" in ret["image"]:
            ret["image"] = ret["image"].replace("localhost", "3.38.100.94")
        return {"user": ret}


class CustomAllAuthPasswordResetForm(AllAuthPasswordResetForm):

    def clean_email(self):
        """
        Invalid email should not raise error, as this would leak users
        for unit test: test_password_reset_with_invalid_email
        """
        email = self.cleaned_data["email"]
        email = get_adapter().clean_email(email)
        self.users = filter_users_by_email(email, is_active=True)
        return self.cleaned_data["email"]

    def save(self, request, **kwargs):
        current_site = get_current_site(request)
        email = self.cleaned_data['email']
        token_generator = kwargs.get('token_generator', default_token_generator)

        for user in self.users:
            temp_key = token_generator.make_token(user)
            custom_password_reset_url = 'https://wafmate/fragment/emailauthenticate2301061457/'
            path = f"{custom_password_reset_url}/{user_pk_to_url_str(user)}/{temp_key}/"
            url = build_absolute_uri(request, path)
            # Values which are passed to password_reset_key_message.txt
            context = {
                "current_site": current_site,
                "user": user,
                "password_reset_url": url,
                "request": request,
                "path": path,
            }

            if app_settings.AUTHENTICATION_METHOD != app_settings.AuthenticationMethod.EMAIL:
                context['username'] = user_username(user)
            get_adapter(request).send_mail(
                'accounts/email/password_reset_key', email, context
            )

        return self.cleaned_data['email']


class CustomPasswordResetSerializer(PasswordResetSerializer):
    @property
    def password_reset_form_class(self):
        return CustomAllAuthPasswordResetForm
