from .models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True
    )

    class Meta:

        model = User

        fields = [
            "id",
            "first_name",
            "email",
            "mobile",
            "password"
        ]


    def create(self, validated_data):

        user = User.objects.create_user(

            first_name = validated_data["first_name"],
            email = validated_data["email"],
            mobile = validated_data["mobile"],
            password = validated_data["password"]

        )

        return user


class LoginSerializer(serializers.Serializer):


    login = serializers.CharField()

    password = serializers.CharField(
        write_only=True
    )

    def validate(self, data):


        login = data.get("login")
        password = data.get("password")

        user = None

        if "@" in login:

            user = authenticate(

                email=login,
                password=password

            )


        else:

            try:

                user = User.objects.get(
                    mobile=login
                )

                if not user.check_password(password):

                    user = None

            except User.DoesNotExist:

                user = None

        if not user:
            raise serializers.ValidationError(

                "Invalid credentials"

            )

        refresh = RefreshToken.for_user(user)

        return {

            "user":{

                "id": user.id,
                "first_name": user.first_name,
                "email": user.email,
                "mobile": user.mobile

            },

            "access": str(refresh.access_token),
            "refresh": str(refresh)

        }

class LogoutSerializer(serializers.Serializer):

    refresh = serializers.CharField()

    def validate(self, data):

        try:

            token = RefreshToken(
                data["refresh"]
            )

            token.blacklist()

        except Exception:

            raise serializers.ValidationError(
                "Invalid token"
            )

        return data