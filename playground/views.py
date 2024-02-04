from django.shortcuts import render
from django.db.models import Q, F, Value, Func, ExpressionWrapper, DecimalField
from django.db.models.functions import Concat
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from django.contrib.contenttypes.models import ContentType
from django.db import transaction, connection


from store.models import Product, Customer, Collection, Order, OrderItem
# from tags.models import TaggedItem

# Create your views here.

#Simple filtering
#def say_hello(request):
    # customers = Customer.objects.filter(email__icontains='.com')
    # colections = Collection.objects.filter(featured_product__isnull=True)
    # products = Product.objects.filter(inventory__lt=10)
    # orders = Order.objects.filter(customer_id=1)
    # orderitems = OrderItem.objects.filter(quantity=3)
    # return render(request,'hello.html',{'name':"Avijit",'customers':list(customers)})
    # return render(request,'hello.html',{'name':"Avijit",'colections':list(colections)})
    # return render(request,'hello.html',{'name':"Avijit",'products':list(products)})
    # return render(request,'hello.html',{'name':"Avijit",'orders':list(orders)})
    # return render(request,'hello.html',{'name':"Avijit",'orderitems':list(orderitems)})

#Complex Filtering
#def say_hello(request):
    # products = Product.objects.filter(inventory__lt=10).filter(unit_price__lt=20)
    # return render(request,'hello.html',{'name':"Avijit",'products':list(products)})

#Q class for getting data
#def say_hello(request):
    # products = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))
    # return render(request,'hello.html',{'name':"Avijit",'products':list(products)})

#F class for comparing different label/column
#def say_hello(request):
    # products = Product.objects.filter(inventory=F('unit_price'))
    # return render(request,'hello.html',{'name':"Avijit",'products':list(products)})

#Sorting data ('-' for decendending orders)
#def say_hello(request):
    # products = Product.objects.order_by('unit_price','-title').reverse()
    # return render(request,'hello.html',{'name':"Asvijit",'products':list(products)})


#Limiting results
# def say_hello(request):
#     products = Product.objects.all()[10:20]
#     return render(request,'hello.html',{'name':"Avijit",'products':list(products)})


#Selecting fields to query
# def say_hello(request):
#     products = Product.objects.values_list('id','title','collection__title')
#     return render(request,'hello.html',{'name':"Avijit",'products':list(products)})


#Deferring Fields
# def say_hello(request):
#     products = Product.objects.only('id','title')
#     return render(request,'hello.html',{'name':"Avijit",'products':list(products)})

#Deferring Fields
# def say_hello(request):
#     products = Product.objects.defer('description')
#     return render(request,'hello.html',{'name':"Avijit",'products':list(products)})

#Selecting related objects
# def say_hello(request):
#     #Select releted(1)
#     products = Product.objects.select_related('collection').all()
#     return render(request,'hello.html',{'name':"Avijit",'products':list(products)})

#Selecting related objects
# def say_hello(request):
#     products = Product.objects.prefetch_related('promotions').all()
#     return render(request,'hello.html',{'name':"Avijit",'products':list(products)})

#Selecting related objects
# def say_hello(request):
#     products = Product.objects.prefetch_related('promotions').select_related('collection').all()
#     return render(request,'hello.html',{'name':"Avijit",'products':list(products)})

#Aggregate
# def say_hello(request):
#     products = Product.objects.aggregate(count=Count('id'), min_price = Min('unit_price'))
#     return render(request,'hello.html',{'name':"Avijit",'products':products})

#Annotate
# def say_hello(request):
#     # products = Product.objects.annotate(is_new=True) #it will not work
#     # products = Product.objects.annotate(is_new=Value(True))
#     products = Product.objects.annotate(new_id=F('id'))
#     return render(request,'hello.html',{'name':"Avijit",'products':products})


# #Calling DB function
# def say_hello(request):
#     #Without Concat class
#     # products = Customer.objects.annotate(
#     #     full_name=Func(F('first_name'),Value(' '), F('last_name'),function='CONCAT')
#     # )
    
#     #With Concat class
#     products = Customer.objects.annotate(
#         full_name=Concat('first_name',Value(' '), 'last_name')
#     )
#     return render(request,'hello.html',{'name':"Avijit",'products':products})

# #Grouping data
# def say_hello(request):

#     products = Customer.objects.annotate(
#         orders_count=Count('order')
#     )
#     return render(request,'hello.html',{'name':"Avijit",'products':products})

#Expression Wrapper for complex querying
# def say_hello(request):
#     discounted_price = ExpressionWrapper(F('unit_price')*0.8, output_field=DecimalField())
#     products = Product.objects.annotate(discounted_price = discounted_price)
#     return render(request,'hello.html',{'name':"Avijit",'products':products})

# #Generic Relationship querying
# def say_hello(request):
    
#     content_type = ContentType.objects.get_for_model(Product)
#     products = TagItem.objects.select_related('tag')\
#     .filter(
#         content_type = content_type,
#         object_id = 1
#     )
#     return render(request,'hello.html',{'name':"Avijit",'products':list(products)})

# #Custom manager| Check the tag model
# def say_hello(request):
#     products = TagItem.objects.get_tags_for(Product, 1)
#     return render(request,'hello.html',{'name':"Avijit",'products':list(products)})


# #Queryset cache
# def say_hello(request):
#     products = Product.objects.all()
#     list(products)
#     list(products) #This won't do anything due to queryset chache.
#     return render(request,'hello.html',{'name':"Avijit"})


# #Creating object/ sending data to the db/ Insert data

# def say_hello(request):
#     collection = Collection()
#     collection.title = 'Game Items'
#     collection.featured_product = Product(pk=1)
#     # collection.featured_product_id = 1 ##This one is same as the previous line of code.
#     collection.save()
#     return render(request,'hello.html',{'name':"Avijit"})

# #Creating object/ Update

# def say_hello(request):
#     collection = Collection(pk=11)
#     collection.title = 'Game' ##If we do not add this line we may lose our data
#     collection.featured_product = None
#     # collection.featured_product_id = 1 ##This one is same as the previous line of code.
#     collection.save()
#     return render(request,'hello.html',{'name':"Avijit"})


#Creating object/ Delete

# def say_hello(request):
    # collection = Collection(pk=11)
    # collection.delete() #Straight forward
    ##If we do not add this line we may lose our data
    # collection.title = 'Game' 
    # collection.featured_product = None
    # collection.featured_product_id = 1 ##This one is same as the previous line of code.
    # collection.save()
    # Collection.objects.filter(id__gt=5).delete()
    # return render(request,'hello.html',{'name':"Avijit"})


#Transaction
# @transaction.atomic()
# def say_hello(request):
    
#     with transaction.atomic():
#         order = Order()
#         order.customer_id = 1
#         order.save()
        
#         item = OrderItem()
#         item.order = order
#         item.product_id = 1
#         item.quantity = 1
#         item.unit_price = 10
#         item.save()
#     return render(request,'hello.html',{'name':"Avijit"})


#Executing Raw SQL queries
# def say_hello(request):
#     # queryset = Product.objects.raw('SELECT * FROM store_product')
#     with connection.cursor() as cursor:
#         cursor.execute('')
#         cursor.close()
#     return render(request,'hello.html',{'name':"Avijit"})

#Executing Raw SQL queries
def say_hello(request):
    return render(request,'hello.html',{'name':"Avijit"})





##Exercise

#Products that have been ordered and sort them by title
# def say_hello(request):
#     products = Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')
#     return render(request,'hello.html',{'name':"Avijit",'products':list(products)})

#Get the last 5 orders with their customer and items (include product)
# def say_hello(request):
#     #orderitem_set is for django convention name but we can set the name as well.
#     products = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]
#     return render(request,'hello.html',{'name':"Avijit",'products':list(products)})

#Aggregate Exercise
# def say_hello(request):
    # products = Order.objects.aggregate(count=Count('id'))
    # products = OrderItem.objects.filter(product__id=1).aggregate(unit_solds=Sum('quantity'))
    # products = Order.objects.filter(customer__id=1).aggregate(count=Count('id'))
    # products = Product.objects.filter(collection__id=3).aggregate(min_price=Min('unit_price'), Avg_price=Avg('unit_price'), max_price=Min('unit_price'))
    # return render(request,'hello.html',{'name':"Avijit",'products':products})