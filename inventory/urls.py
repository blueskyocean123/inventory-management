from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("api/v1/", include("core.api.urls", namespace="core_api")),
    path("api/v1/", include("purchase.api.urls", namespace="purchase_api")),
    path("api/v1/", include("sell.api.urls", namespace="sell_api")),
    path("", include("core.urls", namespace="core")),
    path("", include("purchase.urls", namespace="purchase")),
    path("", include("sell.urls", namespace="sell")),
    path("", include("order.urls", namespace="order")),
]

admin.site.site_header = "Inventory Admin Panel"
admin.site.index_title = "Inventory management"

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
