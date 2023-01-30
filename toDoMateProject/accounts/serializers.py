from allauth.account import app_settings as allauth_settings
from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress
from allauth.utils import email_address_exists
from django.contrib.auth import authenticate
from django.contrib.auth.forms import SetPasswordForm
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import datetime
from rest_framework import serializers
from dj_rest_auth.serializers import LoginSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
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
