from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from purchase.models import *
from purchase.api.serializers import *


class PurchaseProductListCreate(generics.ListCreateAPIView):
    ''' 
        create view
    '''
    model = PurchaseProduct
    serializer_class = PurchaseProductSerializer
    queryset = PurchaseProduct.objects.filter(status=True)
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)


class PurchaseProductDetail(generics.RetrieveUpdateDestroyAPIView):
    ''' 
        detail view
    '''
    model = PurchaseProduct
    serializer_class = PurchaseProductEditSerializer
    queryset = PurchaseProduct.objects.filter(status=True)
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(added_by=self.request.user)
