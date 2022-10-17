from django.urls import path, include
from .views import *

app_name = "sell"

urlpatterns = [
    path("customer/", CustomerCreateView.as_view(), name="customer"),
    path("customer/<int:pk>/", SingleCustomerView.as_view(), name="single-customer"),
    path("customer/edit/<int:pk>/", CustomerUpdateView.as_view(), name="customer-edit"),
    path(
        "customer/delete/<int:pk>/",
        CustomerDeleteView.as_view(),
        name="customer-delete",
    ),
    path("sale/create/", SellProductCreateView.as_view(), name="sale-create"),
    path("sale/edit/<pk>/", SellProductUpdateView.as_view(), name="sale-edit"),
    path("sale/delete/<pk>/", SellProductDeleteView.as_view(), name="sale-delete"),
    path("sales/", SellProductListView.as_view(), name="sales"),
]
