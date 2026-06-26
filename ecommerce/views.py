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
    BrandCreateSerializer,
    CategoryCreateSerializer
)
from .models import (
    Brand,
    Category,
    Product
)
from rest_framework.parsers import (
    MultiPartParser,
    FormParser
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

   
    parser_classes = [
        MultiPartParser,
        FormParser
    ]
    @extend_schema(
        request=BrandCreateSerializer,
        responses=BrandSerializer
    )
    def post(self, request):

        serializer = BrandCreateSerializer(
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

class BrandDetailView(APIView):

    def get_object(self,pk):

        try:

            return Brand.objects.get(
                id=pk
            )

        except Brand.DoesNotExist:

            return None

    @extend_schema(
        responses=BrandSerializer,
        description="Get brand by id"
    )
    def get(self,request,pk):

        brand = self.get_object(pk)

        if not brand:

            return Response(
                {
                    "message":"Brand not found"
                },
                status=404
            )

        serializer = BrandSerializer(
            brand
        )

        return Response(serializer.data)

    parser_classes = [
        MultiPartParser,
        FormParser
    ]
    @extend_schema(
        request=BrandCreateSerializer,
        responses=BrandSerializer,
        description="Update brand"
    )
    def put(self,request,pk):

        brand=self.get_object(pk)

        if not brand:

            return Response(
                {"message":"Brand not found"},
                status=404
            )

        serializer=BrandCreateSerializer(
            brand,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(

            BrandSerializer(
                serializer.instance
            ).data,

            status=status.HTTP_200_OK
        )

        return Response(
            serializer.errors,
            status=400
        )

    @extend_schema(
        description="Delete brand"
    )
    def delete(self,request,pk):

        brand=self.get_object(pk)

        if not brand:

            return Response(
                {"message":"Brand not found"},
                status=404
            )

        brand.delete()

        return Response(
            {
                "message":"Brand deleted"
            }
        )

class CategoryListView(APIView):

    @extend_schema(
        responses=CategorySerializer(many=True),
        description="Get all categories"
    )
    def get(self,request):

        categories=Category.objects.all()

        serializer=CategorySerializer(
            categories,
            many=True
        )

        return Response(serializer.data)

    parser_classes = [
        MultiPartParser,
        FormParser
    ]

    @extend_schema(
        request=CategoryCreateSerializer,
        responses=CategorySerializer,
        description="Create category with image upload"
    )
    
    def post(self,request):

        serializer=CategoryCreateSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(

                CategorySerializer(
                    serializer.instance
                ).data,

                status=status.HTTP_201_CREATED
            )


        return Response(
            serializer.errors,
            status=400
        )

class CategoryDetailView(APIView):

    def get_object(self,pk):

        try:

            return Category.objects.get(
                id=pk
            )

        except Category.DoesNotExist:

            return None


    parser_classes = [
        MultiPartParser,
        FormParser
    ]

    @extend_schema(
        responses=CategorySerializer,
        description="Get category by id"
    )
    def get(self,request,pk):

        category=self.get_object(pk)

        if not category:

            return Response(
                {"message":"Category not found"},
                status=404
            )

        serializer=CategorySerializer(
            category
        )

        return Response(serializer.data)



    @extend_schema(
    request=CategoryCreateSerializer,
    responses=CategorySerializer,
    description="Update category with image upload"
    ) 
    def put(self,request,pk):

        category=self.get_object(pk)

        serializer=CategorySerializer(
            category,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data
            )

        return Response(
            serializer.errors,
            status=400
        )

    @extend_schema(
        description="Delete category"
    )
    def delete(self,request,pk):

        category=self.get_object(pk)

        category.delete()

        return Response(
            {
                "message":"Category deleted"
            }
        )

class ProductListView(APIView):

    @extend_schema(
        responses=ProductSerializer(many=True),
        description="Get all active products"
    )
    def get(self,request):

        products=Product.objects.filter(
            is_active=True
        )

        serializer=ProductSerializer(
            products,
            many=True
        )

        return Response(serializer.data)

    
    @extend_schema(
        request=ProductSerializer,
        responses=ProductSerializer,
        description="Create product"
    )
    def post(self,request):

        serializer=ProductSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=201
            )

        return Response(
            serializer.errors,
            status=400
        )


class ProductDetailView(APIView):

    def get_object(self,pk):

        try:

            return Product.objects.get(
                id=pk
            )

        except Product.DoesNotExist:

            return None

    @extend_schema(
        responses=ProductSerializer,
        description="Get product by id"
    )
    def get(self,request,pk):

        product=self.get_object(pk)

        if not product:

            return Response(
                {"message":"Product not found"},
                status=404
            )

        serializer=ProductSerializer(product)

        return Response(serializer.data)
    
    @extend_schema(
        request=ProductSerializer,
        responses=ProductSerializer,
        description="Update product"
    )
    def put(self,request,pk):

        product=self.get_object(pk)

        serializer=ProductSerializer(
            product,
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data
            )

        return Response(
            serializer.errors,
            status=400
        )

    @extend_schema(
        description="Delete product"
    )
    def delete(self,request,pk):

        product=self.get_object(pk)
        product.delete()

        return Response(
            {
                "message":"Product deleted"
            }
        )