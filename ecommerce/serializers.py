from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from .models import (
    User,
    Gender,
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

        try:

            if "@" in login:

                user = User.objects.get(

                    email=login

                )

            else:


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


                "id":user.id,

                "first_name":user.first_name,

                "email":user.email,

                "mobile":user.mobile


            },


            "access":str(refresh.access_token),


            "refresh":str(refresh)


        }



class RefreshTokenSerializer(TokenRefreshSerializer):

    def validate(self, attrs):

        data = super().validate(attrs)

        return {

            "access": data["access"]

        }


class LogoutSerializer(serializers.Serializer):

    refresh = serializers.CharField()


    def validate(self,data):

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


# =========================
# Gender Serializer
# =========================


class GenderSerializer(serializers.ModelSerializer):


    class Meta:

        model = Gender


        fields = [

            "id",

            "name"

        ]

# =========================
# Brand
# =========================


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


# =========================
# Category
# =========================


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


# =========================
# Product Image
# =========================


class ProductImageSerializer(serializers.ModelSerializer):


    class Meta:

        model = ProductImage


        fields = [

            "id",

            "image",

            "is_primary"

        ]


# =========================
# Product GET
# =========================


class ProductSerializer(serializers.ModelSerializer):


    gender = GenderSerializer(
        read_only=True
    )


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


            "gender",


            "brand",


            "category",


            "images"


        ]


# =========================
# Product CREATE / UPDATE
# =========================


class ProductCreateSerializer(serializers.ModelSerializer):


    images = serializers.ListField(

        child=serializers.ImageField(),

        required=False,

        write_only=True

    )



    class Meta:


        model = Product


        fields = [


            "gender",


            "brand",


            "category",


            "name",


            "description",


            "price",


            "discount_price",


            "stock",


            "is_active",


            "images"


        ]




    def create(self, validated_data):


        images = validated_data.pop(
            "images",
            []
        )


        product = Product.objects.create(
            **validated_data
        )



        for image in images:


            ProductImage.objects.create(

                product=product,

                image=image

            )



        return product





    def update(self, instance, validated_data):


        images = validated_data.pop(
            "images",
            []
        )



        for attr,value in validated_data.items():


            setattr(

                instance,

                attr,

                value

            )



        instance.save()



        if images:


            instance.images.all().delete()



            for image in images:


                ProductImage.objects.create(

                    product=instance,

                    image=image

                )



        return instance