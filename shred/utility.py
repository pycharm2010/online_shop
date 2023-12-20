import re
import threading

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework.exceptions import ValidationError

from phonenumbers import parse, is_valid_number

username_regex = re.compile(r"^[a-zA-Z0-9_.-]+$")


def check_phone(phone_number):
    parsed_phone = parse(phone_number, None)

    if is_valid_number(parsed_phone):
        parsed_phone = 'phone'
    else:

        data = {
            'success': False,
            'message': "Telefon nomeringiz noto'ri"
        }
        raise ValidationError(data)

    return parsed_phone


def check_user_type(user_input):
    parsed_phone = parse(user_input, None)
    if is_valid_number(parsed_phone):
        user_input = 'phone'
    elif re.fullmatch(username_regex, user_input):
        user_input = 'username'
    else:
        data = {
            "success": False,
            "message": "Username yoki telefon raqamingiz noto'g'ri"
        }
        raise ValidationError(data)
    return user_input


class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


class Email:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['subject'],
            body=data['body'],
            to=[data['to_email']]
        )
        if data.get('content_type') == "html":
            email.content_subtype = 'html'
        EmailThread(email).start()


def send_email(email, code):
    html_content = render_to_string(
        'email/authentication/activate_account.html',
        {"code": code}
    )
    Email.send_email(
        {
            "subject": "Royhatdan otish",
            "to_email": email,
            "body": html_content,
            "content_type": "html"
        }
    )

# def send_phone_code(phone, code):
#     account_sid = config('account_sid')
#     auth_token = config('auth_token')
#     client = Client(account_sid, auth_token)
#     client.messages.create(
#         body=f"Salom do'stim! Sizning tasdiqlash kodingiz: {code}\n",
#         from_="+99899325242",
#         to=f"{phone}"
#     )
