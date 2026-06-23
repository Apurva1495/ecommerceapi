from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, email, mobile, password=None):

        if not email:
            raise ValueError("Email required")

        user = self.model(
            email=email,
            mobile=mobile
        )

        user.set_password(password)
        user.save()

        return user


    def create_superuser(self,email,mobile,password):

        user = self.create_user(
            email,
            mobile,
            password
        )

        user.is_staff=True
        user.is_superuser=True

        user.save()

        return user



class User(AbstractBaseUser, PermissionsMixin):

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
        "mobile"
    ]


    objects = UserManager()


    def __str__(self):
        return self.email