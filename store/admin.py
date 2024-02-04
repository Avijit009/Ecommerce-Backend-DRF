from typing import Any, List, Optional, Tuple
from django.contrib import admin, messages
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.utils.html import format_html, urlencode
from django.urls import reverse


from . import models

# Register your models here.

@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title','products_count']
    search_fields = ['title']
    
    @admin.display(ordering='products_count')
    def products_count(self,collection):
        url = (reverse('admin:store_product_changelist') + '?'+ urlencode(
            {
                'collection__id':str(collection.id)
            }
        ))
        return format_html('<a href="{}">{} Products </a>',url, collection.products_count)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count = Count('products')
        )

#Custom filter in the list page
class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'
    

    def lookups(self, request, model_admin):
        return [
            ('<10','Low'),
            ('>10','Ok')
        ]
    def queryset(self, request, queryset:QuerySet):
        if self.value()=='<10':
            return queryset.filter (inventory__lt=10)
    

@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['product']
    autocomplete_fields = ['collection']
    # fields = ['title','slug']
    prepopulated_fields = {
        'slug':['title']
    }
    actions = ['clear_inventory']
    list_display = ['title','slug','unit_price','inventory_status','collection_title']
    list_editable = ['unit_price']
    list_filter = ['collection','last_update',InventoryFilter]
    list_per_page = 10
    list_select_related = ['collection']
    
    def collection_title(self,product):
        return product.collection.title
    #Adding computed columns.
    @admin.display(ordering='inventory')
    def inventory_status(self,product):
        if product.inventory<10:
            return 'Low'
        else:
            return 'Ok'
    
    #Adding custom action
    @admin.action(description='Clear Inventory')
    def clear_inventory(self,request,queryset:QuerySet):
        updated_count= queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated.',
            messages.ERROR
        )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','membership', 'customer_order']
    list_editable = ['membership']
    list_per_page = 10
    list_select_related = ['user']
    autocomplete_fields = ['user']
    # ordering = ['first_name','last_name']
    ordering = ['user__first_name','user__last_name']
    search_fields = ['first_name__istartswith','last_name__istartswith']
    
    #To show customer order
    @admin.display(ordering='customer_order')
    def customer_order(self,order):
        return order.customer_order
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            customer_order = Count('order')
        )

class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    model = models.OrderItem
    extra = 1

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    # search_fields = []
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    list_display = ['id','placed_at','customer']