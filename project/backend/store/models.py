from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Provider(User):
    name = models.CharField(max_length=250, default='')
    phone = models.CharField(max_length=250, default='')
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Provider'
        verbose_name_plural = 'Providers'


class Consumer(User):
    name = models.CharField(max_length=250, default='')
    phone = models.CharField(max_length=250, default='')
    address = models.TextField(default='')
    geo_location = models.CharField(max_length=250, default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Consumer'
        verbose_name_plural = 'Consumers'


class Category(models.Model):
    name = models.CharField(max_length=250, default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    name = models.CharField(max_length=250, default='')
    image = models.ImageField(upload_to='media', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return '%s (%s)' % (self.name, self.category)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class Store(models.Model):
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Store'
        verbose_name_plural = 'Stores'


class Order(models.Model):
    STATUS = (
        ('new', 'new order'),
        ('pending', 'pending order'),
        ('finished', 'finished order')
    )
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, default='new', choices=STATUS)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    ammount = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Order product'
        verbose_name_plural = 'Order products'
