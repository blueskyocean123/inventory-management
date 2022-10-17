from django.urls import path
from core.api.views import *

app_name = "core_api"


urlpatterns = [
    path("warehouse", WarehouseListCreate.as_view(), name="warehouse-list"),
    path("warehouse/<int:pk>", WarehouseDetail.as_view(), name="warehouse-detail"),
    path("category", CategoryListCreate.as_view(), name="category-list"),
    path("category/<int:pk>", CategoryDetail.as_view(), name="category-detail"),
    path("subcategory", SubcategoryListCreate.as_view(), name="subcategory-list"),
    path(
        "subcategory/<int:pk>", SubcategoryDetail.as_view(), name="subcategory-detail"
    ),
    path("product", ProductListCreate.as_view(), name="product-list"),
    path("product/<int:pk>", ProductDetail.as_view(), name="product-detail"),
]
