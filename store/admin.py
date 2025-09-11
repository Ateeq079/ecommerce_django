from itertools import count
from django.contrib import admin , messages
from . import models 
from django.db.models import Count
from django.db.models.query import QuerySet
from django.utils.html import format_html
from django.utils.http import urlencode
from django.urls import reverse
# Register your models here.
##Class for custom filter for searching Inventory filter
class InventoryFilter(admin.SimpleListFilter):
    title = 'Inventory'
    parameter_name = 'inventory'
    def lookups(self, request, model_admin):
        return {("<10", 'Needs Refil'), ("<30", "Low")}
    def queryset(self, request, queryset: QuerySet):
        print("my print :- ",self.value())
        if self.value() == "<10":
            return queryset.filter(inventory__lte = 10)
        elif self.value() == "<30":
            return queryset.filter(inventory__gt = 10).filter(inventory__lte = 30)
##class for Tagsearch

### Product Admin
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug': ['title']
    }
    list_display = ['title','unit_price', 'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_per_page = 30
    search_fields = ['title']
    list_filter = ['collection', InventoryFilter]
    list_select_related = ['collection']
    actions = ['clear_inventory']
    def collection_title(self, product):
        return product.collection.title
    @admin.display(ordering="inventory")
    def inventory_status(self, product): 
        if product.inventory <= 10:
            return 'Needs Refil'
        elif product.inventory <= 30:
            return 'Low'
        return 'OK'
    @admin.action(description='Clear Inventory')
    def clear_inventory(self, request, queryset):
        updated_count =  queryset.update(inventory = 0)
        self.message_user(request, f"{updated_count} products inventory was deleted", messages.ERROR)


##Inline class for OrderAdmin CLass
class OrderItemInline(admin.TabularInline):
    model = models.OrderItem
    extra = 0
    min_num  = 1    
    autocomplete_fields = ['product']
@admin.register(models.Order)
#Decorater & Class for Order Model
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    list_display = ['pk','customer', 'placed_at', 'payment_status']
    ordering = ['id']
    inlines = [OrderItemInline]
    list_per_page = 10


#Decorater & Class for Collection Model
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']
    @admin.display(ordering="products_count")
    def products_count(self, collection):
        url = reverse("admin:store_product_changelist") + "?" + urlencode({"collection__id":str(collection.id)})
        return format_html("<a href='{}'>{}</a>", url, collection.products_count)
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(products_count = Count('products'))


#Decorater & Class for Customer Model
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'order_status']
    list_editable = ['membership']
    # ordering = ['first_name', 'last_name']
    list_per_page = 50
    search_fields = ["first_name__istartswith",]  ##"last_name__istartswith"
    @admin.display(ordering="order_status")
    def order_status(self, customer):
        url = reverse("admin:store_order_changelist") + '?' + urlencode({"customer_id":str(customer.id)})
        return format_html("<a href='{}'>{}</a>", url, customer.order_status)
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(order_status = Count('order'))