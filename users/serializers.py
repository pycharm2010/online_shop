from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import AccessToken

from shred.utility import check_email_phone_number, send_email, check_user_type
from users.models import User, VIA_PHONE, CODE_VERIFIED, NEW, DONE, VIA_EMAIL


class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = User
        fields = ("id", "username")


class SignUpSerializers(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    def __init__(self, *args, **kwargs):
        super(SignUpSerializers, self).__init__(*args, **kwargs)
        self.fields['email_phone_number'] = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = (
            "id",
            "auth_type",
            "auth_status",

        )
        extra_kwargs = {
            "auth_type": {"read_only": True, "required": False},
            "auth_status": {"read_only": True, "required": False},
        }

    def create(self, validated_data):
        user = super(SignUpSerializers, self).create(validated_data)

        if user.auth_type == VIA_PHONE:
            code = user.create_verify_code(VIA_PHONE)
            send_email(user.phone, code)

        if user.auth_type == VIA_EMAIL:
            code = user.create_verify_code(VIA_EMAIL)
            send_email(user.email, code)

        user.save()
        return user

    def validate(self, data):
        super(SignUpSerializers, self).validate(data)
        data = self.auth_validate(data)

        return data

    @staticmethod
    def auth_validate(data):
        user_input = str(data.get("email_phone_number")).lower()

        input_type = check_email_phone_number(user_input)

        if input_type == "phone":

            if User.objects.filter(phone=user_input).exists():
                data = {
                    "success": False,
                    "message": "Bu email alla qachon ro'yhatdan o'tgan"
                }
                raise ValidationError(data)

            data = {
                "phone": user_input,
                "auth_type": VIA_PHONE
            }

        elif input_type == 'email':

            if User.objects.filter(email=user_input).exists():
                data = {
                    "success": False,
                    "message": "Bu email alla qachon ro'yhatdan o'tgan"
                }
                raise ValidationError(data)

            data = {
                'email': user_input,
                'auth_type': VIA_EMAIL
            }

        else:
            data = {
                "success": False,
                "message": "You must send email or phone number"
            }
            raise ValidationError(data)
        return data

    def to_representation(self, instance):
        data = super(SignUpSerializers, self).to_representation(instance)
        data.update(instance.token())

        return data


class ChangeUserInformation(serializers.Serializer):
    first_name = serializers.CharField(write_only=True, required=True)
    last_name = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        password = data.get("password", None)
        confirm_password = data.get("confirm_password", None)
        if password != confirm_password:
            raise ValidationError(
                {"message": "Parolingiz va tasdiqlash parolingiz bir-biriga teng emas"}
            )
        if password:
            validate_password(password)
            validate_password(confirm_password)

        return data

    def validate_username(self, username):
        if len(username) < 5 or len(username) > 30:
            raise ValidationError(
                {"message": "Username must be between 5 and 30 characters long"}
            )
        elif username.isdigit():
            raise ValidationError({"message": "This username is entirely numeric"})
        elif User.objects.filter(username=username).exists():
            data = {
                'message': " Bu username royhatdan o'tgan "
            }
            raise ValidationError(data)
        return username

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.password = validated_data.get("password", instance.password)
        instance.username = validated_data.get("username", instance.username)
        if validated_data.get("password"):
            instance.set_password(validated_data.get("password"))
        if instance.auth_status == CODE_VERIFIED:
            instance.auth_status = DONE
        instance.save()
        return instance


class LoginSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super(LoginSerializer, self).__init__(*args, **kwargs)
        self.fields["user_input"] = serializers.CharField(required=True)
        self.fields["username"] = serializers.CharField(required=False, read_only=True)

    def auth_validate(self, data):
        user_input = str(data.get("user_input"))

        if check_user_type(user_input) == "username":
            username = user_input
        elif check_user_type(user_input) == "phone":
            user = self.get_user(phone=user_input)
            username = user.username
        else:
            data = {
                "success": True,
                "message": "Siz email, username yoki telefon raqami jonatishingiz kerak",
            }
            raise ValidationError(data)

        authentication_kwargs = {
            self.username_field: username,
            "password": data["password"],
        }
        current_user = User.objects.filter(username__iexact=username).first()
        if current_user is not None and current_user.auth_status in [
            NEW,
            CODE_VERIFIED,
        ]:
            raise ValidationError(
                {"success": False, "message": "Siz royhatdan toliq otmagansiz!"}
            )
        user = authenticate(**authentication_kwargs)
        if user is not None:
            self.user = user
        else:
            raise ValidationError(
                {
                    "success": False,
                    "message": "Sorry, login or password you entered is incorrect. Please check and trg again!",
                }
            )

    def validate(self, data):
        self.auth_validate(data)
        if self.user.auth_status not in [DONE]:
            raise PermissionDenied("Siz login qila olmaysiz. Ruxsatingiz yoq")
        data = self.user.token()
        data['auth_status'] = self.user.auth_status
        data['full_name'] = self.user.full_name
        return data

    def get_user(self, **kwargs):
        user = User.objects.filter(**kwargs)

        if not user.exists():
            data = {"message": "No activate account"}
            raise ValidationError(data)
        return user.first()


class LoginRefreshSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        access_token_instance = AccessToken(data['access'])
        user_id = access_token_instance['user_id']
        user = get_object_or_404(User, id=user_id)
        update_last_login(None, user)
        return data


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class ResetPasswordSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    password = serializers.CharField(min_length=8, required=True, write_only=True)
    confirm_password = serializers.CharField(min_length=8, required=True, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'password', 'confirm_password')

    def validate(self, data):
        password = data.get('password', None)
        confirm_password = data.get('confirm_password', None)
        if password != confirm_password:
            data = {
                "success": False,
                "message": "Parollaringiz qiymati bir-biriga teng emas"
            }
            raise ValidationError(data)
        if password:
            validate_password(password)
            return data

    def update(self, instance, validated_data):
        password = validated_data.pop('password')
        instance.set_password(password)
        super(ResetPasswordSerializer, self).update(validated_data, instance)

