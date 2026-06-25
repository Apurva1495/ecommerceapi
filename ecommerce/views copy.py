from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    LogoutSerializer,
    ProductSerializer,
    BrandSerializer,
    CategorySerializer,
    ProductSerializer
)
from .models import (
    Brand,
    Category,
    Product
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
    

class ProductListView(APIView):

    @extend_schema(

        responses=ProductSerializer,

        description="Get all active products"

    )
    def get(self, request):

        products = Product.objects.filter(
            is_active=True
        )

        serializer = ProductSerializer(
            products,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

class BrandListView(APIView):

    @extend_schema(
        responses=BrandSerializer(many=True),
        description="Get all brands"
    )

    def get(self, request):
        brands = Brand.objects.all()
        serializer = BrandSerializer(
            brands,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

class CategoryListView(APIView):

    @extend_schema(
        responses=CategorySerializer(many=True),
        description="Get all categories"
    )

    def get(self,request):
        categories = Category.objects.all()
        serializer = CategorySerializer(
            categories,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

class ProductListView(APIView):

    @extend_schema(
        responses=ProductSerializer(many=True),
        description="Get all products with brand category and images"
    )

    def get(self,request):
        products = Product.objects.filter(
            is_active=True
        )

        serializer = ProductSerializer(
            products,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

class ProductDetailView(APIView):

    @extend_schema(
        responses=ProductSerializer,
        description="Get product details by id"
    )

    def get(self,request,pk):

        try:
            product = Product.objects.get(
                id=pk,
                is_active=True
            )

        except Product.DoesNotExist:

            return Response(
                {
                    "message":"Product not found"
                },

                status=status.HTTP_404_NOT_FOUND
            )

        serializer = ProductSerializer(
            product
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )        