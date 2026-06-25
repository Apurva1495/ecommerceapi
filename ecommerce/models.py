from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager



class UserManager(BaseUserManager):

    def create_user(
        self,
        first_name,
        email,
        mobile,
        password=None
    ):

        if not email:
            raise ValueError("Email required")


        user = self.model(

            first_name=first_name,

            email=email,

            mobile=mobile

        )


        user.set_password(password)

        user.save()

        return user



    def create_superuser(
        self,
        first_name,
        email,
        mobile,
        password
    ):


        user = self.create_user(

            first_name,

            email,

            mobile,

            password

        )


        user.is_staff=True

        user.is_superuser=True


        user.save()


        return user





class User(AbstractBaseUser, PermissionsMixin):


    first_name = models.CharField(
        max_length=100
    )


    email = models.EmailField(
        unique=True
    )


    mobile = models.CharField(
        max_length=15,
        unique=True
    )


    is_verified = models.BooleanField(
        default=False
    )


    is_active=models.BooleanField(
        default=True
    )


    is_staff=models.BooleanField(
        default=False
    )


    created_at=models.DateTimeField(
        auto_now_add=True
    )



    USERNAME_FIELD = "email"


    REQUIRED_FIELDS = [
        "first_name",
        "mobile"
    ]



    objects = UserManager()



    def __str__(self):

        return self.email


class Brand(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )


    logo = models.ImageField(
        upload_to="brands/",
        null=True,
        blank=True
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    updated_at = models.DateTimeField(
        auto_now=True
    )


    def __str__(self):

        return self.name

class Category(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )


    image = models.ImageField(
        upload_to="categories/",
        null=True,
        blank=True
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):

        return self.name

class Product(models.Model):


    brand = models.ForeignKey(

        Brand,

        on_delete=models.CASCADE,

        related_name="products"

    )


    category = models.ForeignKey(

        Category,

        on_delete=models.CASCADE,

        related_name="products"

    )


    name = models.CharField(
        max_length=200
    )


    description = models.TextField()


    price = models.DecimalField(

        max_digits=10,

        decimal_places=2

    )


    discount_price = models.DecimalField(

        max_digits=10,

        decimal_places=2,

        null=True,

        blank=True

    )


    stock = models.PositiveIntegerField(

        default=0

    )


    is_active = models.BooleanField(

        default=True

    )


    created_at=models.DateTimeField(

        auto_now_add=True

    )


    updated_at=models.DateTimeField(

        auto_now=True

    )


    def __str__(self):

        return self.name

class ProductImage(models.Model):


    product = models.ForeignKey(

        Product,

        on_delete=models.CASCADE,

        related_name="images"

    )


    image = models.ImageField(

        upload_to="products/"

    )


    is_primary = models.BooleanField(

        default=False

    )


    created_at=models.DateTimeField(

        auto_now_add=True

    )


    def __str__(self):

        return self.product.name                