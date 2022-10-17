from django.urls import path
from purchase.api.views import *

app_name = 'purchase_api'


urlpatterns = [
    path('purchase/products', PurchaseProductListCreate.as_view(), name='product-list'),
    path('purchase/product/<int:pk>', PurchaseProductDetail.as_view(), name='product-detail'),
]
