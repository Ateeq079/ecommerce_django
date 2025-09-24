from rest_framework.response import Response
from rest_framework import status
from .models import Product, Collection , OrderItem, ReviewModel , Cart
from .serializers import ProductSerializer, CollectionSerializer, ReviewSerializer, CartSerializer
from django.db.models import Count
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter
from rest_framework.filters import SearchFilter

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()    
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['title']
    
    def get_serializer_context(self):
        return {"request": self.request}
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id = kwargs['pk']).count() > 0:
            return Response(
                {"error": "Product cant be deleted it is associated with a order"},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count("products")).all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id = kwargs['pk']).count() > 0:
            return Response(
                {"error": "Collection can't be deleted because it has products in it."},
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return ReviewModel.objects.filter(product_id=self.kwargs['product_pk'])
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
class CartView(ModelViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()