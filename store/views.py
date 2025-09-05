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
from .serializers import ProductSerialzier
@api_view()
def product_list(request):
    queryset = Product.objects.all()
    serializer = ProductSerialzier(queryset, many=True)
    return Response(serializer.data)

@api_view()
def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    serializer = ProductSerialzier(product)
    return Response(serializer.data)


