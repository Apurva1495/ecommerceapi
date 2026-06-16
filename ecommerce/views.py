from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import (
    extend_schema,
)
from .serializers import RegisterSerializers ,LoginSerializers
from rest_framework import status


class RegisterView(APIView):

    @extend_schema(
            request=RegisterSerializers,
            responses=RegisterSerializers
    )
    def post(self, request):

        serializers = RegisterSerializers(
            data=request.data
        )

        if serializers.is_valid():

            serializers.save()

            return Response(
                serializers.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializers.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):

    @extend_schema(
            request=LoginSerializers,
            responses=LoginSerializers
    )
    def post(self,request):
        serializers = LoginSerializers(
            data=request.data
        )

        if serializers.is_valid():
               return Response(serializers.validated_data,status=status.HTTP_200_OK)
        

        return Response(
         serializers.errors,
         status=status.HTTP_400_BAD_REQUEST   
        )