# views.py
import boto3
from botocore.exceptions import ClientError
from allauth.account.models import EmailAddress
from dj_rest_auth.serializers import PasswordResetSerializer
from dj_rest_auth.views import UserDetailsView, sensitive_post_parameters_m
import datetime
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import generics, status
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser
from .models import User, Code
from .permissions import IsCreator, IsCreatorOrReadOnly
from .serializers import UserDetailSerializer, CustomUserDetailSerializer, UserImageSerializer, \
    CustomRegisterSerializer, CodeSerializer, PasswordResetConfirmSerializer

# Social Login
from dj_rest_auth.registration.views import SocialLoginView, SocialConnectView, ResendEmailVerificationView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

# Google
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter

# Kakao
from allauth.socialaccount.providers.kakao import views as kakao_view

from .utils import send_verification_mail


# Registration
class RegisterView(CreateAPIView):
    serializer_class = CustomRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        send_verification_mail(email)
        serializer.save(request)
        data = {'detail': _('Verification e-mail sent.')}
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_200_OK, headers=headers)


class RegisterConfirmView(APIView):
    def post(self, request):
        serializer = CodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not Code.objects.filter(code=serializer.validated_data['code'],
                                   email=serializer.validated_data['email']).exists():
            return Response({'code': 'Incorrect value.'}, status=status.HTTP_400_BAD_REQUEST)

        code = Code.objects.get(code=serializer.validated_data['code'], email=serializer.validated_data['email'])
        if timezone.now()-code.created_at > datetime.timedelta(minutes=5):
            code.delete()
            return Response({'code': 'The code is expired.'}, status=status.HTTP_400_BAD_REQUEST)

        code.delete()
        user = EmailAddress.objects.get(email=serializer.validated_data['email'])
        user.verified = True
        user.save()
        return Response({'message': 'The user account has been created successfully.'}, status=status.HTTP_201_CREATED)


# Password reset
class PasswordResetView(GenericAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        # Create a serializer with request.data
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        send_verification_mail(email)
        # Return the success message with OK HTTP status
        return Response(
            {'detail': _('Password reset e-mail has been sent.')},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'detail': _('Password has been reset with the new password.')},
        )


# Resend email verification mail
class CustomResendEmailVerificationView(ResendEmailVerificationView):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not EmailAddress.objects.filter(**serializer.validated_data).exists():
            return Response({"email": "This email address is not registered."},
                            status=status.HTTP_404_NOT_FOUND)

        email = serializer.validated_data["email"]
        send_verification_mail(email)
        return Response({'detail': _('ok')}, status=status.HTTP_200_OK)


# Custom User Detail
class CustomUserDetailsView(UserDetailsView):
    serializer_class = CustomUserDetailSerializer


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
    parser_classes = [MultiPartParser, FormParser]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        image_name = 'media/' + f'{instance.id}' + '.jpg'
        s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        try:
            image = s3.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=image_name)
            return HttpResponse(image['Body'].read(), content_type='image/')
        except ClientError as e:
            error_code = e.response["ResponseMetadata"]["HTTPStatusCode"]
            if error_code == 404:
                try:
                    image = s3.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key='media/default.jpg')
                    return HttpResponse(image['Body'].read(), content_type='image/jpeg')
                except:
                    return Response('A default image is not uploaded.', status=status.HTTP_404_NOT_FOUND)
            return Response(e, status=error_code)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        image_file = request.data.get('image')
        s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
        bucket = settings.AWS_STORAGE_BUCKET_NAME
        image_name = 'media/' + f'{instance.id}' + '.jpg'
        try:
            s3.head_object(Bucket=bucket, Key=image_name)
            s3.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=image_name)
        except ClientError as e:
            error_code = e.response["ResponseMetadata"]["HTTPStatusCode"]
            if error_code != 404:
                return Response(e, status=error_code)

        s3.upload_fileobj(image_file, settings.AWS_STORAGE_BUCKET_NAME, image_name)
        return Response(status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        bucket = settings.AWS_STORAGE_BUCKET_NAME
        image_name = 'media/' + f'{instance.id}' + '.jpg'
        s3 = boto3.client('s3', aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

        try:
            s3.head_object(Bucket=bucket, Key=image_name)
            s3.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=image_name)
        except ClientError as e:
            error_code = e.response["ResponseMetadata"]["HTTPStatusCode"]
            return Response(e, status=error_code)

        return Response(status=status.HTTP_204_NO_CONTENT)
