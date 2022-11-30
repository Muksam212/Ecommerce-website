from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class DateTimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True


class Customer(DateTimeStamp):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customers")
    full_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100, null=True, blank=True)
    joined_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    def __str__(self):
        return "{}".format(self.full_name)


class Category(DateTimeStamp):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering=('-created_at',)
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return "{}".format(self.title)

class Product(DateTimeStamp):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/images", blank=True, null=True)
    marked_price = models.PositiveIntegerField(default=0, blank=True,null=True)
    selling_price = models.PositiveIntegerField(default=0, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    warranty = models.CharField(max_length=100, null=True, blank=True)
    return_policy = models.CharField(max_length=100, blank=True, null=True)
    view_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return "{}".format(self.title)



class Cart(DateTimeStamp):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ('-created_at',)
        verbose_name = "Cart"
        verbose_name_plural = "Carts"

    def __str__(self):
        return "Cart: "+str(self.id)

class CartProduct(DateTimeStamp):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    sub_total = models.PositiveIntegerField()

    class Meta:
        ordering = ('-created_at',)
        verbose_name = "CartProduct"
        verbose_name_plural = "CartProducts"

    def __str__(self):
        return "Cart: "+str(self.id) + "CartProduct: "+str(self.id)


ORDER_STATUS = (
    ("Order Received","Order Received"),
    ("Order Processing","Order Processing"),
    ("On the Way","On the way"),
    ("Order Completed","Order Completed"),
    ("Order Canceled","Order Canceled")
)

class Order(DateTimeStamp):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    ordered_by = models.CharField(max_length=100)
    shipping_address = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    email = models.EmailField(null=True, blank=True)
    sub_total = models.PositiveIntegerField()
    discount = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    order_status = models.CharField(max_length=100, choices=ORDER_STATUS)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Order"
        verbose_name_plural = "Orders"

    def __str__(self):
        return "Cart: "+str(self.id)