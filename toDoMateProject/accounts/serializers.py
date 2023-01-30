from allauth.socialaccount.models import SocialAccount
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.forms import SetPasswordForm
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import datetime
from rest_framework import serializers
from dj_rest_auth.serializers import LoginSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer, SocialLoginSerializer
from google.oauth2 import id_token
from google.auth.transport import requests
from .models import User, Code


class CustomRegisterSerializer(RegisterSerializer):
    username = None
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

        try:
            id_token = attrs['id_token']
        except KeyError:
            raise serializers.ValidationError(
                _('Incorrect input. id_token is required.'),
            )

        CLIENT_ID = settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['client_id']
        idinfo = id_token.verify_oauth2_token(id_token, requests.Request(), CLIENT_ID)
        uid = idinfo['sub']
        email = idinfo['email']
        email_verified = idinfo['email_verified']
        if not email_verified:
            raise serializers.ValidationError(
                _('Email is not verified.')
            )
        if not email or not uid:
            raise serializers.ValidationError(
                _('Incorrect id_token.')
            )


        attrs = {**attrs, 'uid': uid, 'email': email}
        return attrs

    def create(self, validated_data):
        uid = validated_data.get('uid')
        email = validated_data.get('email')
        extra_data = {'email': email}
        SocialAccount(extra_data=extra_data, uid=uid, provider='google')







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
