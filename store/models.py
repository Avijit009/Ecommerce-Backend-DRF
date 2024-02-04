from django.contrib import admin
from uuid import uuid4
from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.

'''
Relationships in this db

Collection = Product (One to Many)
Customer = Order (One to Many) or Order = Customer (One to Many)
Order = Item (One to Many)
Cart = Item (One to Many)
Address = Customer (One to Many)

Promotion = Product (Many to Many)

Collection to Product has CIRCULAR DEPENDENCY.
Change the class to a string to remove the error on circular dependency.


'''

class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()
    

class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product',on_delete=models.SET_NULL,null=True,related_name='+',blank=True)
    
    def __str__(self) -> str:
        return self.title
    class Meta:
        ordering = ['title']

class Product(models.Model):
    #sku = models.CharField(max_length=10,primary_key=True)
    title = models.CharField(max_length=150)
    slug = models.SlugField()
    description = models.TextField(null=True,blank=True)
    unit_price = models.DecimalField(
        max_digits=6,
        decimal_places=2, 
        validators=[MinValueValidator(1)]
        )
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection,on_delete=models.PROTECT,related_name='products')
    promotions = models.ManyToManyField(Promotion, blank=True)
    
    def __str__(self) -> str:
        return self.title
    class Meta:
        ordering = ['title']
    
class Customer(models.Model):
    MEMBERSHIPS_GOLD = 'G'
    MEMBERSHIPS_SILVER = 'S'
    MEMBERSHIPS_BRONZE = 'B'
    MEMBERSHIPS_CHOICES =[
        (MEMBERSHIPS_GOLD,'Gold'),
        (MEMBERSHIPS_SILVER,'Silver'),
        (MEMBERSHIPS_BRONZE,'Bronze'),
    ]
    '''This first_name, last_name, email are already there in the User class'''
    # first_name = models.CharField(max_length=150)
    # last_name = models.CharField(max_length=150)
    # email = models.EmailField(unique=True)
    
    phone = models.CharField(max_length=150)
    birth_date = models.DateField(null=True, blank=True)
    membership = models.CharField(max_length=1,choices=MEMBERSHIPS_CHOICES,default=MEMBERSHIPS_BRONZE)
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'
    
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name
    
    class Meta:
        ordering = ['user__first_name', 'user__last_name']
        permissions = [
            ('view_history','Can view history')
        ]
    
    # def __str__(self) -> str:
    #     return f'{self.first_name} {self.last_name}'
    # class Meta:
    #     ordering = ['first_name', 'last_name']

class Order(models.Model):
    placed_at = models.DateTimeField(auto_now_add=True)
    PENDING_STATUS = 'P'
    COMPLETED_STATUS = 'C'
    FAILED_STATUS = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PENDING_STATUS,'Pending'),
        (COMPLETED_STATUS,'Completed'),
        (FAILED_STATUS,'Failed'),
    ]
    payment_status = models.CharField(max_length=1,choices=PAYMENT_STATUS_CHOICES,default=PENDING_STATUS)
    customer = models.ForeignKey(Customer,on_delete=models.PROTECT)
    class Meta:
        permissions = [
            # code name followed by Description
            ('cancel_order','Can cancel order')
        ]

class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.PROTECT,related_name='items')
    product = models.ForeignKey(Product,on_delete=models.PROTECT,related_name='orderitems')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6,decimal_places=2)

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    zip = models.CharField(max_length=10)


class Cart(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    
    class Meta:
        unique_together = [['cart','product']]


class Review (models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='reviews')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)