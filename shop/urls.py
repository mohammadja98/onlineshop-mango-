from django.urls import include, path
from .views import CategoryListView, CommentCreateView, ProductDetailView, ProductListView, CategoryDetailView

app_name = "shop" 

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('category/', CategoryListView.as_view(), name='category_list'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('comment/<int:product_id>/', CommentCreateView.as_view(), name='comment_create'),

]
