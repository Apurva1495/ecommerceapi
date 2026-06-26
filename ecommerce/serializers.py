from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import (
    User,
    Brand,
    Category,
    Product,
    ProductImage
)


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
   
class BrandSerializer(serializers.ModelSerializer):


    class Meta:

        model = Brand

        fields = [
            "id",
            "name",
            "logo"
        ]


class BrandCreateSerializer(serializers.ModelSerializer):

    logo = serializers.ImageField(
        required=False
    )


    class Meta:

        model = Brand

        fields = [
            "name",
            "logo"
        ]        

class CategorySerializer(serializers.ModelSerializer):

    class Meta:

        model = Category

        fields = [
            "id",
            "name",
            "image"
        ]

class CategoryCreateSerializer(serializers.ModelSerializer):

    image = serializers.ImageField(
        required=False
    )


    class Meta:

        model = Category

        fields = [
            "name",
            "image"
        ]

class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:

        model = ProductImage

        fields = [
            "id",
            "image",
            "is_primary"
        ]

class ProductSerializer(serializers.ModelSerializer):


    brand = BrandSerializer(
        read_only=True
    )


    category = CategorySerializer(
        read_only=True
    )


    images = ProductImageSerializer(
        many=True,
        read_only=True
    )


    class Meta:

        model = Product


        fields = [

            "id",

            "name",

            "description",

            "price",

            "discount_price",

            "stock",

            "is_active",

            "brand",

            "category",

            "images"

        ]
class ProductCreateSerializer(serializers.ModelSerializer):

    images = serializers.ListField(
        child=serializers.ImageField(),
        required=False,
        write_only=True
    )

    class Meta:

        model = Product

        fields = [

            "brand",
            "category",
            "name",
            "description",
            "price",
            "discount_price",
            "stock",
            "is_active",
            "images",

        ]        
