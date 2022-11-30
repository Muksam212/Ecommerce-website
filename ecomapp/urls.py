from django.urls import path
from ecomapp.views import (HomePageView, AboutPageView, ContactPageView, BasePage,
                        AllProductView,ProductDetailView,AddToCart,MyCart,ManageCartView)

app_name = "ecomapp"

urlpatterns = [
    path("base/", BasePage.as_view(), name="base_page"),
    path("about/", AboutPageView.as_view(), name="about_page"),
    path("contact/", ContactPageView.as_view(), name="contact_us"),
    path("", HomePageView.as_view(), name="home_page"),

    path("all-product/", AllProductView.as_view(), name="all_product_view"),
    path("product/<slug:slug>/", ProductDetailView.as_view(), name="product_detail_view"),
    path("add-to-cart/<int:pro_id>/", AddToCart.as_view(), name="add_to_cart"),
    path('my-cart/', MyCart.as_view(), name="my_cart"),
    path("manage-cart/<int:object_id>/", ManageCartView.as_view(), name="manage_cart")

]