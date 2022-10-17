from django.urls import path, include
from .views import *

app_name = "order"

urlpatterns = [
    # path("orders/", AllOrdersView.as_view(), name="all-orders"),
    path("order-list/", OrderListView.as_view(), name="order-list"),
    path(
        "order-create/<int:product_id>/", OrderCreateView.as_view(), name="order-create"
    ),
    path("order-edit/<int:pk>/", OrderUpdateView.as_view(), name="order-edit"),
    path("order-delete/<int:pk>/", OrderDeleteView.as_view(), name="order-delete"),
    path("order-sell/<int:pk>/", SellOrderItem.as_view(), name="sell-order"),
]
