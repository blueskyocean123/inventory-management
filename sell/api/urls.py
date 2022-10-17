from django.urls import path
from sell.api.views import *

app_name = "sell_api"


urlpatterns = [
    path("customer", CustomerSingleObject.as_view(), name="customer"),
    path("customers", CustomerListCreate.as_view(), name="customer-list"),
    path("customers/<int:pk>", CustomerDetail.as_view(), name="customer-detail"),
    path("sell/products", SellProductListCreate.as_view(), name="product-list"),
    path("sell/product/<int:pk>", SellProductDetail.as_view(), name="product-detail"),
    path("sell", SellView.as_view(), name="sell"),
]
