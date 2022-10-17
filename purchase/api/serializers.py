from rest_framework import serializers
from purchase.models import *


# Create serializer
class PurchaseProductSerializer(serializers.ModelSerializer):
    '''
        create serializer
    '''
    class Meta:
        model = PurchaseProduct
        exclude = [
            'added_by',
            'status',
            'date_added',
            'date_updated'
        ]


# Create serializer
class PurchaseProductEditSerializer(serializers.ModelSerializer):
    '''
        edit serializer
    '''
    class Meta:
        model = PurchaseProduct
        exclude = [
            'date_added',
            'date_updated'
        ]
