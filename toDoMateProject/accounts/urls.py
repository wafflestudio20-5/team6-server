from dj_rest_auth.views import PasswordResetView, PasswordResetConfirmView, PasswordChangeView, LoginView, LogoutView, UserDetailsView
from dj_rest_auth.registration.views import VerifyEmailView, RegisterView
from django.urls import include, path, re_path
from django.conf import settings
from .views import GoogleToDjangoLogin, google_login, google_callback, CustomVerifyEmailView

urlpatterns = [
    # URLs that do not require a session or valid token
    path('registration/', RegisterView.as_view(), name='registration'),
    path('account-confirm-email/', CustomVerifyEmailView.as_view(), name='account_email_verification_sent'),
    # 배포 시에는 client url로 redirect해야 할 것 같습니다.
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$', CustomVerifyEmailView.as_view(),
     name='account_confirm_email'),
    path('password/reset/', PasswordResetView.as_view(), name='password_reset'),
    # 배포 시에는 client url로 redirect해야 할 것 같습니다.
    path('password/reset/confirm/<uid>/<token>', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view()),
    path('login/', LoginView.as_view(), name='login'),
    # URLs that require a user to be logged in with a valid session / token.
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/', UserDetailsView.as_view(), name='user_details'),
    # path('password/change/', PasswordChangeView.as_view(), name='password_change'),
    # Google Login
    path('google/login', google_login),
    path('google/callback', google_callback),
    path('google/login/django', GoogleToDjangoLogin.as_view())

]

if getattr(settings, 'REST_USE_JWT', False):
    from rest_framework_simplejwt.views import TokenVerifyView

    from dj_rest_auth.jwt_auth import get_refresh_view

    urlpatterns += [
        path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
        path('token/refresh/', get_refresh_view().as_view(), name='token_refresh'),
    ]