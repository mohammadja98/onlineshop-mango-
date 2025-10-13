from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _



class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = RichTextField()    
    image = models.ImageField(verbose_name=_('Category Image'), upload_to='category/category_cover/', blank=True, )

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("shop:category_detail", args=[self.pk])
    

class Discount(models.Model):
    discount = models.FloatField()
    description = models.CharField(max_length=255)

    def __str__(self):
        return f'{str(self.discount)} | {self.description}'

class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    slug = models.SlugField(unique=True, allow_unicode=True)
    price = models.IntegerField()
    description = RichTextField()
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(verbose_name=_('Product Image'), upload_to='product/product_cover/', blank=True, )
    discounts = models.ManyToManyField(Discount, blank=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:product_detail', args = [self.slug])
    

# Custom Manager    
class ActiveCommentsManager(models.Manager):
    def get_queryset(self):
        return super(ActiveCommentsManager, self).get_queryset().filter(active=True)
    

class Comment(models.Model):
    PRODUCT_STARS = [
        ('1', _('Very Bad')),
        ('2', _('Bad')),
        ('3', _('Normal')),
        ('4', _('Good')),
        ('5', _('Perfect')),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments', verbose_name=_('comment author'))
    body = models.TextField(verbose_name=_('comment text'))
    detetime_created = models.DateTimeField(auto_now_add=True)
    datetime_updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    # Custom Manager    
    objects = models.Manager()
    active_comments_manager = ActiveCommentsManager()