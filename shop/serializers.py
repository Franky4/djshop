from django.db.models import Q
from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from photologue.models import Gallery, Photo

from .models import Product, Category


class PhotoSer(serializers.ModelSerializer):
    """Изображения"""
    class Meta:
        model = Photo
        fields = ('image',)


class CatSer(serializers.ModelSerializer):
    """Категории"""
    children = serializers.ListField(source='get_children', read_only=True, child=RecursiveField(),)

    class Meta:
        model = Category
        fields = ('name', 'children',)


class ProductSer(serializers.ModelSerializer):
    """Сериализация продуктов"""
    photo = PhotoSer()

    class Meta:
        model = Product
        fields = (
            'title',
            'description',
            'price',
            'slug',
            'availability',
            'quantity',
            'photo'
        )
