from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework import permissions
from core.models import *
from core.api.serializers import *


class WarehouseListCreate(generics.ListCreateAPIView):
    ''' 
        create view
    '''
    model = Warehouse
    serializer_class = WarehouseSerializer
    queryset = Warehouse.objects.filter(status=True)
    # permission_classes = [permissions.IsAuthenticated]


class WarehouseDetail(generics.RetrieveUpdateDestroyAPIView):
    ''' 
        detail view
    '''
    model = Warehouse
    serializer_class = WarehouseEditSerializer
    queryset = Warehouse.objects.filter(status=True)
    # permission_classes = [permissions.IsAuthenticated]


class CategoryListCreate(generics.ListCreateAPIView):
    ''' 
        create view
    '''
    model = Category
    serializer_class = CategorySerializer
    queryset = Category.objects.filter(status=True)
    # permission_classes = [permissions.IsAuthenticated]


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    ''' 
        detail view
    '''
    model = Category
    serializer_class = CategoryEditSerializer
    queryset = Category.objects.filter(status=True)


class SubcategoryListCreate(generics.ListCreateAPIView):
    ''' 
        create view
    '''
    model = Subcategory
    serializer_class = SubcategorySerializer
    queryset = Subcategory.objects.filter(status=True)


class SubcategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    ''' 
        detail view
    '''
    model = Subcategory
    serializer_class = SubcategoryEditSerializer
    queryset = Subcategory.objects.filter(status=True)


class ProductListCreate(generics.ListCreateAPIView):
    ''' 
        create view
    '''
    model = Product
    serializer_class = ProductSerializer
    queryset = Product.objects.filter(status=True)

    def perform_create(self, serializer):
        serializer.save(added_by=self.request.user)


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    ''' 
        detail view
    '''
    model = Product
    serializer_class = ProductEditSerializer
    queryset = Product.objects.filter(status=True)

    def perform_update(self, serializer):
        serializer.save(added_by=self.request.user)
