import requests
from allauth.account import app_settings as allauth_settings
from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress
from allauth.socialaccount.helpers import complete_social_login
from allauth.utils import email_address_exists
from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import SetPasswordForm
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from requests.exceptions import HTTPError
import datetime
from rest_framework import serializers
from dj_rest_auth.serializers import LoginSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer, SocialLoginSerializer, SocialConnectMixin
from .models import User, Code


class CustomRegisterSerializer(RegisterSerializer):
    username = None

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                if EmailAddress.objects.get(email=email).verified:
                    raise serializers.ValidationError(
                        _('A user is already registered with this e-mail address.'),
                    )
                raise serializers.ValidationError(
                    _('This e-mail address has attempted registration but failed. Please resend the verification email.')
                )
        return email

    def get_cleaned_data(self):
        return {
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
        }


class CodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Code
        fields = ['code', 'email']


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


class GoogleLoginSerializer(SocialLoginSerializer):
    def validate(self, attrs):
        view = self.context.get('view')
        request = self._get_request()

        if not view:
            raise serializers.ValidationError(
                _('View is not defined, pass it as a context variable'),
            )

        adapter_class = getattr(view, 'adapter_class', None)
        if not adapter_class:
            raise serializers.ValidationError(_('Define adapter_class in view'))

        adapter = adapter_class(request)
        app = adapter.get_provider().get_app(request)

        # More info on code vs access_token
        # http://stackoverflow.com/questions/8666316/facebook-oauth-2-0-code-and-token

        access_token = attrs.get('access_token')
        code = attrs.get('code')
        # Case 1: We received the access_token
        if access_token:
            tokens_to_parse = {'access_token': access_token}
            token = access_token
            # For sign in with apple
            id_token = attrs.get('id_token')
            if id_token:
                tokens_to_parse['id_token'] = id_token

        # Case 2: We received the authorization code
        elif code:
            google_info = settings.SOCIALACCOUNT_PROVIDERS['google']
            client_id = google_info['APP']['client_id']
            client_secret = google_info['APP']['secret']
            callback_url = 'https://wafmate.com/fragment/mainpage/oauth'

            token_req = requests.post(
                f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={callback_url}")
            token_req_json = token_req.json()
            error = token_req_json.get("error")
            if error:
                raise serializers.ValidationError(error)

            access_token = token_req_json.get('access_token')
            token = access_token
            tokens_to_parse = {'access_token': access_token}

        else:
            raise serializers.ValidationError(
                _('Incorrect input. access_token or code is required.'),
            )

        social_token = adapter.parse_token(tokens_to_parse)
        social_token.app = app

        try:
            login = self.get_social_login(adapter, app, social_token, token)
            complete_social_login(request, login)
        except HTTPError:
            raise serializers.ValidationError(_('Incorrect value'))

        if not login.is_existing:
            # We have an account already signed up in a different flow
            # with the same email address: raise an exception.
            # This needs to be handled in the frontend. We can not just
            # link up the accounts due to security constraints
            if allauth_settings.UNIQUE_EMAIL:
                # Do we have an account already with this email address?
                account_exists = get_user_model().objects.filter(
                    email=login.user.email,
                ).exists()
                if account_exists:
                    raise serializers.ValidationError(
                        _('User is already registered with this e-mail address.'),
                    )

            login.lookup()
            login.save(request, connect=True)

        attrs['user'] = login.account.user

        return attrs


class GoogleConnectSerializer(SocialConnectMixin, GoogleLoginSerializer):
    pass


class PasswordResetConfirmSerializer(serializers.Serializer):
    """
    Serializer for confirming a password reset attempt.
    """
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)
    email = serializers.EmailField()
    code = serializers.IntegerField()

    set_password_form_class = SetPasswordForm

    _errors = {}
    user = None
    set_password_form = None

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if not email:
                raise serializers.ValidationError(
                    _('This field is required.')
                )
            if not email_address_exists(email):
                raise serializers.ValidationError(
                    _('A user is not registered.')
                )
        return email

    def validate(self, attrs):
        code = attrs.get("code")
        email = attrs.get("email")
        if not Code.objects.filter(code=code,
                                   email=email).exists():
            raise serializers.ValidationError('The code and email does not match.')

        code = Code.objects.get(code=code, email=email)
        if timezone.now() - code.created_at > datetime.timedelta(minutes=5):
            code.delete()
            raise serializers.ValidationError('The code is expired.')

        code.delete()
        self.user = User._default_manager.get(email=email)
        # Construct SetPasswordForm instance
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs,
        )
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)

        return attrs

    def save(self):
        return self.set_password_form.save()


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'nickname', 'detail']


class CustomUserDetailSerializer(UserDetailSerializer):
    def to_internal_value(self, data):
        data = data.get("user")
        return super().to_representation(data)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        return {"user": ret}


class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['image']
