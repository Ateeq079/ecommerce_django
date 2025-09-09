from django.shortcuts import render
# from django.http import HttpResponse
# # Create your views here.
# def product_list(request):
#     return HttpResponse("HEllO WORLD")
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Product
from .serializers import ProductSerializer
@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        queryset = Product.objects.select_related("collection").all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('OK')


@api_view()
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)


