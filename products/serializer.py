from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name")
    class Meta:
        model = Product
        fields = "__all__"