from django.urls import path

from .views import (

    RegisterView,
    LoginView,
    LogoutView,
    RefreshTokenView,

    BrandListView,
    BrandDetailView,

    CategoryListView,
    CategoryDetailView,

    ProductListView,
    ProductDetailView,

    GenderListView,

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
        "v1/token/refresh/",
        RefreshTokenView.as_view()
    ),
    

     path(
        'v1/genders/',
        GenderListView.as_view(),
        name='genders'
    ),

    path(
        'v1/brands/',
        BrandListView.as_view(),
        name='brands'
    ),

    path(
        'v1/brands/<int:pk>/',
        BrandDetailView.as_view(),
        name='brand-detail'
    ),

    path(
        'v1/categories/',
        CategoryListView.as_view(),
        name='categories'
    ),

    path(
        'v1/categories/<int:pk>/',
        CategoryDetailView.as_view(),
        name='category-detail'
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