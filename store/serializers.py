from rest_framework import serializers
from .models import Product, Collection
from decimal import Decimal


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "title"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "slug",
            "unit_price",
            "inventory",
            "price_with_tax",
            "collection",
        ]

    price_with_tax = serializers.SerializerMethodField("calculate_tax")

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
