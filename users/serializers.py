from turtledemo.__main__ import DONE

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from shred.utility import check_phone, send_email, check_user_type
from users.models import User, VIA_PHONE, CODE_VERIFIED, NEW


class SignUpSerializers(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    def __init__(self, *args, **kwargs):
        super(SignUpSerializers, self).__init__(*args, **kwargs)
        self.fields['phone'] = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            'id',
            'auth_type',
            'auth_status',

        )
        extra_kwargs = {
            'auth_type': {'read_only': True, 'required': False},
            'auth_status': {'read_only': True, 'required': False}
        }

    def create(self, validated_data):
        user = super(SignUpSerializers, self).create(validated_data)
        if user.auth_type == VIA_PHONE:
            code = user.create_verify_code(VIA_PHONE)
            send_email(user.phone, code)
        user.save()
        return user

    def validate(self, data):
        super(SignUpSerializers, self).validate(data)
        data = self.auth_validate(data)

        return data

    @staticmethod
    def auth_validate(data):
        user_input = data.get('phone')
        print('phone number', user_input)
        input_type = check_phone(user_input)

        if input_type == 'phone':
            if User.objects.filter(phone=user_input).exists():
                raise ValidationError({
                    "success": False,
                    "message": "Bu telefon raqami allaqachon ma'lumotlar bazasida bor"
                })
            data = {
                "phone": user_input,
                "auth_type": VIA_PHONE
            }

        else:
            data = {
                'success': False,
                'message': "You must send email or phone number"
            }
            raise ValidationError(data)
        return data

    def to_representation(self, instance):
        data = super(SignUpSerializers, self).to_representation(instance)
        data.update(instance.token())

        return data




