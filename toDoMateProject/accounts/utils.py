import random
from django.conf import settings
from django.core.mail import send_mail

from accounts.models import Code


def generate_activation_code(email):
    code = int(''.join([str(random.randint(0, 9)) for _ in range(6)]))
    Code.objects.filter(email=email).all().delete()
    Code.objects.create(code=code, email=email)
    return code


def send_verification_mail(email):
    generated_code = generate_activation_code(email)
    subject = 'Todomate verification code'
    message = f'인증 번호: {generated_code:06}\n투두메이트 앱에서 위의 번호를 입력하시면 인증이 완료됩니다.\n이메일 인증을 요청하지 않으셨다면 이 메일을 무시하셔도 됩니다.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email, ]
    send_mail(subject, message, from_email, recipient_list)
