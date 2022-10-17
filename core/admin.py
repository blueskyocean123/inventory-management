from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from import_export.admin import ImportExportModelAdmin, ExportActionMixin
from .resources import ProductResource
from .models import *


class ProductAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    def make_status_active(self, modeladmin, request, queryset):
        queryset.update(status=True)

    def make_status_inactive(self, modeladmin, request, queryset):
        queryset.update(status=False)

    make_status_active.short_description = "Update status to active"
    make_status_inactive.short_description = "Update status to inactive"

    list_display = [
        "product_name",
        "category",
        "sell_price",
        "quantity",
        "added_by",
        "status",
    ]
    date_hierarchy = "date_added"
    list_display_links = ["product_name", "added_by"]
    search_fields = ["product_name"]
    actions = [make_status_active, make_status_inactive]

    resource_class = ProductResource


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "organization",
        "is_staff",
    )
    list_filter = ("is_staff", "is_superuser")


# class UserInlineAdmin():
#     model = User
#     inlines = [ProductAdmin]


class SubcategoryAdmin(admin.ModelAdmin):
    # model = Category
    list_display = ["name", "category", "status"]
    search_fields = ["name"]


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "status"]
    search_fields = ["name"]


class WarehouseAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "status"]
    search_fields = ["name"]


# admin.site.register(Chalan)
admin.site.register(Organization)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory, SubcategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Warehouse, WarehouseAdmin)
