from django.shortcuts import get_object_or_404, redirect, render
from django.views import generic
from django.contrib import messages
from django.utils.translation import gettext as _


from cart.forms import AddToCartProductForm
from shop.forms import CommentForm

from .models import Category, Product, Comment

class ProductListView(generic.ListView):
    queryset = Product.objects.filter(available=True)
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
        context["comment_form"] = CommentForm()  
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

    

class CommentCreateView(generic.CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user

        product_id = int(self.kwargs['product_id'])
        product = get_object_or_404(Product, id=product_id)
        obj.product = product
        obj.save()

        messages.success(self.request, _('Your comment has been added successfully.'))

        return redirect('shop:product_detail', slug=product.slug)

    def form_invalid(self, form):
        messages.error(self.request, _('There was an error submitting your comment.'))
        product_id = self.kwargs['product_id']
        product = get_object_or_404(Product, id=product_id)
        return redirect('product_detail', slug=product.slug)
