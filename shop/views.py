from django.shortcuts import render
from django.views import generic

from cart.forms import AddToCartProductForm

from .models import Category, Product

class ProductListView(generic.ListView):
    queryset = Product.objects.filter(available = True)
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    form = AddToCartProductForm(initial={'quantity': 1, 'inplace': False})


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AddToCartProductForm()
        return context

class CategoryListView(generic.ListView):
    queryset = Category.objects.all()
    template_name = 'products/category_list.html'
    context_object_name = 'categories'

class CategoryDetailView(generic.DetailView):
    model = Category
    template_name = 'products/category_detail.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) 
        context['products'] = self.object.products.filter(available=True)
        return context