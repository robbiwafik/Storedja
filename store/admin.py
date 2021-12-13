from django.contrib import admin
from django.db.models import query
from django.urls import reverse
from django.utils.html import format_html, urlencode
from .models import Collection, Customer, Order, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'unit_price',
                    'inventory', 'last_update', 'collection']
    list_per_page = 10


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'featured_product', 'products_count']
    list_per_page = 10

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        query_str = urlencode({'collection__id': str(collection.id)})
        url = reverse('admin:store_product_changelist') + '?' + query_str
        return format_html('<a href="{}">{}</a>', url, collection.products.count())


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'payment_status', 'customer']
    list_per_page = 10


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name',
                    'email', 'phone', 'birth_date', 'membership']
    list_per_page = 10
