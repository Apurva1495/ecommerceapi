from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import (
    extend_schema,
)
from .serializers import RegisterSerializers
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
