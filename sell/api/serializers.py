from django.db.models import fields
from rest_framework import serializers
from sell.models import *


class CustomerSerializer(serializers.ModelSerializer):
    """
    create serializer
    """

    class Meta:
        model = Customer
        exclude = ["status", "date_added"]


class CustomerEditSerializer(serializers.ModelSerializer):
    """
    edit serializer
    """

    class Meta:
        model = Customer
        exclude = ["date_added"]


class SellProductSerializer(serializers.ModelSerializer):
    """
    create serializer
    """

    class Meta:
        model = SellProduct
        exclude = ["added_by", "date_updated", "date_added"]


class SellProductEditSerializer(serializers.ModelSerializer):
    """
    edit serializer
    """

    class Meta:
        model = SellProduct
        exclude = ["added_by", "date_updated", "date_added"]


class SellSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellProduct
        field = ["customer"]
