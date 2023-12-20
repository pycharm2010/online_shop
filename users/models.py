import random
import uuid
from datetime import datetime, timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models

from shred.models import BaseModel
from rest_framework_simplejwt.tokens import RefreshToken

# Create your models here.

NEW, CODE_VERIFIED = ('new', 'code_verified')
ORDINARY_USER, MANAGER, ADMIN = ("ordinary_user", 'manager', 'admin')
VIA_PHONE = ('via_phone',)


class User(BaseModel, AbstractUser):
    USER_ROLES = (
        (ORDINARY_USER, ORDINARY_USER),
        (MANAGER, MANAGER),
        (ADMIN, ADMIN)
    )

    AUTH_STATUS = (
        (NEW, NEW),
        (CODE_VERIFIED, CODE_VERIFIED),
    )

    phone = models.CharField(max_length=13, unique=True)
    user_roles = models.CharField(max_length=31, choices=USER_ROLES, default=ORDINARY_USER)
    auth_status = models.CharField(max_length=31, choices=AUTH_STATUS, default=NEW)
    auth_type = models.CharField(max_length=31, default=VIA_PHONE)

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def create_verify_code(self, verify_type):
        code = "".join([str(random.randint(0, 10000) % 10) for _ in range(4)])
        UserConfirmation.objects.create(
            user_id=self.id,
            verify_type=verify_type,
            code=code
        )
        return code

    def check_username(self):
        if not self.username:
            temp_username = f'instagram-{uuid.uuid4().__str__().split("-")[-1]}'  # instagram-23324fsdf
            while User.objects.filter(username=temp_username):
                temp_username = f"{temp_username}{random.randint(0, 9)}"
            self.username = temp_username

    def check_email(self):
        if self.email:
            normalize_email = self.email.lower()  # aKhamdjon@gmail.com -> akhamdjon@gmail.com
            self.email = normalize_email

    def check_pass(self):
        if not self.password:
            temp_password = f'password-{uuid.uuid4().__str__().split("-")[-1]}'  # 123456mfdsjfkd
            self.password = temp_password

    def hashing_password(self):
        if not self.password.startswith('pbkdf2_sha256'):
            self.set_password(self.password)

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            "access": str(refresh.access_token),
            "refresh_token": str(refresh)
        }

    def save(self, *args, **kwargs):
        self.clean()
        super(User, self).save(*args, **kwargs)

    def clean(self):
        self.check_email()
        self.check_username()
        self.check_pass()
        self.hashing_password()


PHONE_EXPIRE = 2
EMAIL_EXPIRE = 5


class UserConfirmation(BaseModel):
    code = models.CharField(max_length=4)
    verify_type = models.CharField(max_length=31, default=VIA_PHONE)
    user = models.ForeignKey('users.User', models.CASCADE, related_name='verify_codes')
    expiration_time = models.DateTimeField(null=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user.__str__())

    def save(self, *args, **kwargs):
        if self.verify_type == VIA_PHONE:  # 30-mart 11-33 + 5minutes
            self.expiration_time = datetime.now() + timedelta(minutes=PHONE_EXPIRE)
        super(UserConfirmation, self).save(*args, **kwargs)

