from django.contrib import admin

from .models import Product,Category,Comment


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'product', 'body', 'stars', 'datetime_created', 'active']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass