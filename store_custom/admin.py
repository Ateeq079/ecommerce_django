from django.contrib import admin
from store.admin import ProductAdmin
from store.models import Product

from django.contrib.contenttypes.admin import GenericTabularInline
# Register your models here.
from tags.models import TaggedItem

class TagInline(GenericTabularInline):
    model = TaggedItem
    autocomplete_fields = ['tag']

admin.site.unregister(Product)



@admin.register(Product)
class CustomProductAdmin(ProductAdmin):
    inlines = [TagInline]
