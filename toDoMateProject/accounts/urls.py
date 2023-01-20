from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView, LoginView, LogoutView, UserDetailsView
from dj_rest_auth.registration.views import VerifyEmailView, RegisterView, ResendEmailVerificationView
from dj_rest_auth.jwt_auth import get_refresh_view
from rest_framework_simplejwt.views import TokenVerifyView
from django.urls import path, re_path, include
from .views import ConfirmEmailView, GoogleLogin, KakaoLogin, GoogleConnect, KakaoConnect, UserDestroyView

urlpatterns = [
    # Registration
    path('registration/', RegisterView.as_view(), name='registration'),
    path('registration/resend-email', ResendEmailVerificationView.as_view(), name="rest_resend_email"),
    re_path(r'^account-confirm-email/$', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', ConfirmEmailView.as_view(), name='account_confirm_email'),
    # Password
    path('password/reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password/reset/confirm/<uid>/<token>', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view()),
    # Login/logout
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # User detail
    path('user/', UserDetailsView.as_view(), name='user_details'),
    path('user/<int:pk>/', UserDestroyView.as_view(), name='user_delete'),
    # Token
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('token/refresh/', get_refresh_view().as_view(), name='token_refresh'),
    # Social Login
    re_path(r'', include('allauth.urls'), name='socialaccount_signup'),
    path('google/login/', GoogleLogin.as_view(), name='google_login'),
    path('google/connect/', GoogleConnect.as_view(), name='google_connect'),
    path('kakao/login/', KakaoLogin.as_view(), name='kakao_login'),
    path('kakao/connect/', KakaoConnect.as_view(), name='kakao_connect'),
]
