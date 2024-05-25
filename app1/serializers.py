from rest_framework import serializers
from .models import Category,ProductSigns


class CategorySignsSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)

    class Meta:
        model = Category
        fields = '__all__'


class ProductSignsSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    category = serializers.CharField(max_length=100)
    image = serializers.ImageField()
    video = serializers.FileField()
    audio = serializers.FileField()
    doc = serializers.FileField()

    class Meta:
        model = ProductSigns
        fields = '__all__'


