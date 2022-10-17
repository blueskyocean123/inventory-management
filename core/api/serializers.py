from django.template.defaultfilters import slugify

from rest_framework import serializers

from core.models import *


class WarehouseSerializer(serializers.ModelSerializer):
    """
    create serializer
    """

    class Meta:
        model = Warehouse
        exclude = ["status", "date_added"]


class WarehouseEditSerializer(serializers.ModelSerializer):
    """
    Edit serializer
    """

    class Meta:
        model = Warehouse
        exclude = ["date_added"]


class CategorySerializer(serializers.ModelSerializer):
    """
    create serializer
    """

    class Meta:
        model = Category
        exclude = ["status", "date_added"]


class CategoryEditSerializer(serializers.ModelSerializer):
    """
    Edit serializer
    """

    class Meta:
        model = Category
        exclude = ["date_added"]


class SubcategorySerializer(serializers.ModelSerializer):
    """
    Create serializer
    """

    class Meta:
        model = Subcategory
        exclude = ["status", "date_added"]


class SubcategoryEditSerializer(serializers.ModelSerializer):
    """
    edit serializer
    """

    class Meta:
        model = Subcategory
        exclude = ["date_added"]


class ProductSerializer(serializers.ModelSerializer):
    """
    Create serializer
    """

    class Meta:
        model = Product
        exclude = ["status", "date_added", "date_updated"]

    def validate(self, data):
        # check if product already exist
        if "product_name" in data:
            product_instance = Product.objects.filter(
                product_slug=slugify(data["product_name"]),
            )
            if product_instance:
                raise serializers.ValidationError(
                    {"product_name": "Product already exists."}
                )

        return data


class ProductEditSerializer(serializers.ModelSerializer):
    """
    edit serializer
    """

    class Meta:
        model = Product
        exclude = ["date_added", "date_updated"]
