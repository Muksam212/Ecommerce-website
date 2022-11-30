from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView, View
from ecomapp.models import Product, Category, Cart, CartProduct
# Create your views here.

class BasePage(TemplateView):
    template_name = "ecomapp/base.html"

class HomePageView(TemplateView):
    template_name = "ecomapp/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product_list"] = Product.objects.all()
        return context

class AboutPageView(TemplateView):
    template_name = "ecomapp/about.html"


class ContactPageView(TemplateView):
    template_name = "ecomapp/contact_us.html"
    

class AllProductView(TemplateView):
    template_name = "ecomapp/allproduct.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_categories'] = Category.objects.all()
        return context


class ProductDetailView(TemplateView):
    template_name = "ecomapp/product_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        product = Product.objects.get(slug=url_slug)
        product.view_count += 1
        product.save()
        context['product'] = product
        return context


class AddToCart(TemplateView):
    template_name = "ecomapp/add_to_cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #get product id from requested url
        product_id = self.kwargs['pro_id']
       
        product_object = Product.objects.get(id=product_id)
        

        #now checking the session if the cart is exists or not
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart_obj = Cart.objects.get(id=cart_id)
            this_product_in_cart = cart_obj.cartproduct_set.filter(
                product = product_object
            )
            #item already exists in cart
            if this_product_in_cart.exists():
                cartproduct = this_product_in_cart.last()
                cartproduct.quantity += 1
                cartproduct.sub_total += product_object.selling_price
                cartproduct.save()
                cart_obj.total += product_object.selling_price
                cart_obj.save()
            #new items in added in cart
            else:
                cartproduct = CartProduct.objects.create(
                    cart=cart_obj, product=product_object,
                    rate=product_object.selling_price,
                    quantity=1, sub_total=product_object.selling_price
                )
                cart_obj.total += product_object.selling_price
                cart_obj.save()
        else:
            cart_obj = Cart.objects.create(total=0)
            self.request.session['cart_id'] = cart_obj.id
            cartproduct = CartProduct.objects.create(
                    cart=cart_obj, product=product_object,
                    rate=product_object.selling_price,
                    quantity=1, sub_total=product_object.selling_price
                )
            cart_obj.total += product_object.selling_price
            cart_obj.save()
        return context


class MyCart(TemplateView):
    template_name = "ecomapp/my_cart.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_id = self.request.session.get("cart_id", None)
        if cart_id:
            cart = Cart.objects.get(id=cart_id)
        else:
            cart = None
        context["cart"] = cart
        return context

class ManageCartView(View):
    def get(self, request, *args, **kwargs):
        object_id = self.kwargs['object_id']
        action = request.GET.get("action")
        object_id = CartProduct.objects.get(id=object_id)
        cart_object = object_id.cart
        if action == "inc":
            object_id.quantity += 1
            object_id.sub_total += object_id.rate
            object_id.save()
            cart_object.total += object_id.rate
            cart_object.save()
        elif action == "dcr":
            object_id.quantity -= 1
            object_id.sub_total += object_id.rate
            object_id.save()
            cart_object.total += object_id.rate
            cart_object.save()
            if object_id.quantity == 0:
                object_id.delete()
        elif action == "rmv":
            cart_object.total -=  object_id.sub_total
            cart_object.save()
            object_id.delete()
        else:
            pass
        return redirect("ecomapp:my_cart")