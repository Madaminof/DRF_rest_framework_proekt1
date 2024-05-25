from django.shortcuts import render

from .models import Category, ProductSigns
from .serializers import CategorySignsSerializer, ProductSignsSerializer
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response


class CategoryAPI(APIView):
    def get(self, request):
        category = Category.objects.all()
        serializer = CategorySignsSerializer(category, many=True)
        return Response(serializer.data)


class ProductSignsAPI(APIView):
    def get(self, request):
        product = ProductSigns.objects.all()
        serializer = ProductSignsSerializer(product, many=True)
        return Response(serializer.data)


class ProductDetailSignsAPI(APIView):
    def get(self, request, pk):
        product = ProductSigns.objects.get(pk=pk)
        serializer = ProductSignsSerializer(product)
        return Response(serializer.data)
