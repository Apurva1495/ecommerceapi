from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    LogoutSerializer
)


class RegisterView(APIView):

    @extend_schema(

        request=RegisterSerializer,

        responses={
            201: RegisterSerializer
        },

        description="Create new user account"

    )
    def post(self, request):

        serializer = RegisterSerializer(

            data=request.data

        )

        if serializer.is_valid():

            serializer.save()

            return Response(

                serializer.data,
                status=status.HTTP_201_CREATED

            )

        return Response(

            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST

        )

class LoginView(APIView):


    @extend_schema(

        request=LoginSerializer,
        responses={
            200: LoginSerializer

        },

        description="Login using email or mobile and get JWT access and refresh tokens"

    )
    def post(self, request):

        serializer = LoginSerializer(
            data=request.data

        )

        if serializer.is_valid():

            return Response(

                serializer.validated_data,
                status=status.HTTP_200_OK

            )

        return Response(

            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST

        )

class LogoutView(APIView):


    @extend_schema(

        request=LogoutSerializer,
        responses={
            200: {
                "message": "Logout Successfully"
            }
        },

        description="Logout user by blacklisting refresh token"

    )

    def post(self, request):

        serializer = LogoutSerializer(
            data=request.data
        )

        if serializer.is_valid():
            return Response(
                {
                    "message":"Logout Successfully"
                },
                status=status.HTTP_200_OK
            )

        return Response(

            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST

        )