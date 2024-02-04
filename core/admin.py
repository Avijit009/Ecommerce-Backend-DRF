from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import User
from store.models import Product
from store.admin import ProductAdmin
from tags.models import TaggedItem
# Register your models here.

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2",'email','first_name','last_name'),
            },
        ),
    )

class Taginline(GenericTabularInline):
    autocomplete_fields = ['tag']
    model = TaggedItem
    
class CustomProductAdmin(ProductAdmin):
    inlines = [Taginline]
    
admin.site.unregister(Product)
admin.site.register(Product,CustomProductAdmin)