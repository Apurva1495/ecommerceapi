from django.urls import path

from .views import (
    RegisterView,
    LoginView,
    LogoutView,

    BrandListView,
    CategoryListView,
    ProductListView,
    ProductDetailView
)

urlpatterns = [

    path(
        'v1/register/',
        RegisterView.as_view(),
        name='register'
    ),

    path(
        'v1/login/',
        LoginView.as_view(),
        name='login'
    ),

    path(
        'v1/logout/',
        LogoutView.as_view(),
        name='logout'
    ),

    path(
        'v1/brands/',
        BrandListView.as_view(),
        name='brands'
    ),

    path(
        'v1/categories/',
        CategoryListView.as_view(),
        name='categories'
    ),
    path(
        'v1/products/',
        ProductListView.as_view(),
        name='products'
    ),
    path(
        'v1/products/<int:pk>/',
        ProductDetailView.as_view(),
        name='product-detail'
    ),

]