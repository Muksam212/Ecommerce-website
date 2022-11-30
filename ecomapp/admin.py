from django.contrib import admin
from ecomapp.models import (
    Product,
    Customer,
    Category,
    Cart,
    CartProduct,
    Order
)
# Register your models here.

admin.site.register([
    Product,
    Customer,
    Category,
    Cart,
    CartProduct,
    Order
])