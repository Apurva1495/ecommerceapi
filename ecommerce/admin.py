from django.contrib import admin

from .models import (
    Brand,
    Category,
    Product,
    ProductImage
)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "name",
        "logo"
    ]


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)