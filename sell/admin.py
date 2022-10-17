from django.contrib import admin
from .models import Customer, SellProduct


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["name", "phone", "email", "status"]
    list_display_links = ["name", "phone", "email"]
    search_fields = ["phone", "email"]


@admin.register(SellProduct)
class SellProductAdmin(admin.ModelAdmin):
    list_display = ["invoice_number", "customer"]
    search_fields = ["invoice_number"]
    date_hierarchy = "date_added"
    # readonly_fields = ["total_price"]
