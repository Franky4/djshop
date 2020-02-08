from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category, Product, Cart, CartItem, Order


@admin.register(Category)
class Category(MPTTModelAdmin):
    """Category"""
    list_display = ('name', 'parent')
    mptt_level_indent = 20
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class Product(admin.ModelAdmin):
    """Company"""
    list_display = ('title', 'id')
    # list_display_links = ('name',)
    # mptt_level_indent = 20
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Cart)
class Cart(admin.ModelAdmin):
    """Cart"""
    list_display = ('id',
                    'user',
                    )
    list_display_links = ('id', 'user')
    # prepopulated_fields = {'slug': ('id', 'user',)}

@admin.register(CartItem)
class CartItem(MPTTModelAdmin):
    """Type KKM"""
    list_display = ('cart', 'product', 'quantity')
    mptt_level_indent = 20
    # prepopulated_fields = {'slug': ('cart', 'product',)}


@admin.register(Order)
class Order(admin.ModelAdmin):
    """Order"""
    list_display = ('cart', 'accepted', 'date', )
    list_filter = ('accepted',)
    search_fields = ('date',)
    # prepopulated_fields = {'slug': ('cart',)}
    ordering = ['date']
    mptt_level_indent = 20
    # prepopulated_fields = {'slug': ('cart', 'date',)}

# admin.site.register(Category, Category)

