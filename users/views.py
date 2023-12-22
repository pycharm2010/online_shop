import logging
from datetime import datetime
from turtledemo.__main__ import DONE

from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError, PermissionDenied

from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from shred.utility import send_email, check_user_type
from users.models import User, NEW, CODE_VERIFIED, VIA_PHONE
from users.serializers import SignUpSerializers
from rest_framework import serializers


# Create your views here.

class CreateUserAPIView(CreateAPIView):
    queryset = User
    permission_classes = [AllowAny, ]
    serializer_class = SignUpSerializers


class VerifyAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, *args, **kwargs):
        user = self.request.user
        code = self.request.data.get('code')

        self.check_verify(user, code)
        return Response(
            data={
                "success": True,
                "auth_status": user.auth_status,
                "access": user.token()['access'],
                "refresh": user.token()['refresh_token']
            }
        )

    @staticmethod
    def check_verify(user, code):
        verifies = user.verify_codes.filter(expiration_time__gte=datetime.now(), code=code, is_confirmed=False)

        if not verifies.exists():
            data = {
                'success': False,
                "message": "Tasdiqlash kodingiz xato yoki eskirgan"
            }
            raise ValidationError(data)
        else:
            verifies.update(is_confirmed=True)
        if user.auth_status == NEW:
            user.auth_status = CODE_VERIFIED
            user.save()
        return True


class GetNewVerification(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request, *args, **kwargs):

        user = request.user
        print(user, '<=======================================')
        logging.debug(f"User: {user}")
        self.check_verification(user)

        if user.auth_type == VIA_PHONE:
            code = user.create_verify_code(VIA_PHONE)
            send_email(user.phone, code)
        else:
            data = {
                "message": "Telefon raqami notogri"
            }
            raise ValidationError(data)

        return Response(
            {
                "success": True,
                "message": "Tasdiqlash kodingiz qaytadan jo'natildi."
            }
        )

    @staticmethod
    def check_verification(user):
        verifies = user.verify_codes.filter(expiration_time__gte=datetime.now(), is_confirmed=False)
        if verifies.exists():
            data = {
                "message": "Kodingiz hali ishlatish uchun yaroqli. Biroz kutib turing"
            }
            raise ValidationError(data)
