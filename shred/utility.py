import re
import threading

import phonenumbers
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from rest_framework.exceptions import ValidationError

from phonenumbers import parse, is_valid_number

username_regex = re.compile(r"^[a-zA-Z0-9_.-]+$")
phone_regex = re.compile(r"(\+[0-9]+\s*)?(\([0-9]+\))?[\s0-9\-]+[0-9]+")
email_regex = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b")


def check_email_phone_number(email_or_phone_number):
    if re.fullmatch(phone_regex, email_or_phone_number):
        email_or_phone_number = 'phone'
    elif re.fullmatch(email_regex,email_or_phone_number):
        email_or_phone_number = 'email'
    else:
        data = {
            "success": False,
            "message": "Telefon nomeringiz noto'ri"
        }
        raise ValidationError(data)

    return email_or_phone_number


def check_user_type(user_input):
    if re.fullmatch(username_regex, user_input):
        user_input = "username"
    elif re.fullmatch(phone_regex, user_input):
        user_input = 'phone'
    else:
        data = {
            "success": False,
            "message": "Username yoki telefon raqamingiz noto'g'ri",
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
            subject=data["subject"], body=data["body"], to=[data["to_email"]]
        )
        if data.get("content_type") == "html":
            email.content_subtype = "html"
        EmailThread(email).start()


def send_email(email, code):
    html_content = render_to_string(
        "email/authentication/activate_account.html", {"code": code}
    )
    Email.send_email(
        {
            "subject": "Royhatdan otish",
            "to_email": email,
            "body": html_content,
            "content_type": "html",
        }
    )


# def send_phone_code(phone, code):
#
#     account_sid = 'ACf6d5d0e1454cbbcbdcabd784754674ff'
#     auth_token = 'e4b416ce36cd3679248b9baa32e54526'
#     client = Client(account_sid, auth_token)
#
#     client.messages.create(
#         body=f"Salom do'stim! Sizning tasdiqlash kodingiz: {code}\n",
#         from_='+998906757507',
#         to=f"{phone}"
#     )
