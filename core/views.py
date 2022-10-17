from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse
from django.views.generic import (
    View,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView,
    DetailView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin

from .models import *
from .forms import *
from .resources import ProductResource

from sell.models import Customer, SellProduct
from purchase.models import PurchaseProduct
from order.models import Order


@login_required()
def download_product_csv(request):
    product_resource = ProductResource()
    dataset = product_resource.export()
    response = HttpResponse(dataset.csv, content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="product.csv"'
    return response


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.filter(status=True)
        context["products"] = products

        context["total_products"] = products.count()
        context["total_customer"] = Customer.objects.filter(status=True).count()
        context["total_sell"] = SellProduct.objects.all().count()
        context["total_Purchase"] = PurchaseProduct.objects.all().count()
        context["orders"] = Order.objects.filter(order_status=False)
        return context


# =====================
# === Profile Views ===
# =====================


class ProfileView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    template_name = "profile.html"
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_queryset(self):
        return User.objects.filter(username=self.kwargs["username"])

    def test_func(self, *args, **kwargs):
        if self.request.user.username == self.get_object().username:
            return True
        return False


class ProfileEditView(
    LoginRequiredMixin, SuccessMessageMixin, UserPassesTestMixin, UpdateView
):
    template_name = "profile-edit.html"
    model = User
    fields = ["first_name", "last_name", "phone"]
    slug_field = "username"
    slug_url_kwarg = "username"
    success_message = "Profile updated!"

    def get_queryset(self):
        return User.objects.filter(username=self.kwargs["username"])

    def get_success_url(self, **kwargs):
        return reverse("core:profile", kwargs={"username": self.get_object().username})

    def test_func(self, *args, **kwargs):
        if self.request.user.username == self.get_object().username:
            return True
        return False


class UserManagement(LoginRequiredMixin, UserPassesTestMixin, View):
    def get(self, *args, **kwargs):
        users = User.objects.all()
        context = {"users": users}
        return render(self.request, "user-management.html", context)

    def test_func(self, *args, **kwargs):
        if self.request.user.is_staff:
            return True
        return False


class EditUserManagent(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView
):
    model = User
    form_class = UserPermissionForm
    template_name = "edit-user-management.html"
    slug_field = "username"
    slug_url_kwarg = "username"
    success_url = "core:user-management"
    success_message = "Changes saved successfully"

    def get_success_url(self, **kwargs):
        return reverse(self.success_url)

    def test_func(self, *args, **kwargs):
        if self.request.user.is_superuser:
            return True
        return False


# =====================
# === Product Views ===
# =====================


class ProductView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = "product.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = Product.objects.filter(status=True).order_by("-id")
        return context

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False


class ProductCreateView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView
):
    model = Product
    template_name = "product_create.html"
    form_class = ProductForm
    success_url = "core:product-create"
    success_message = "%(product_name)s was created successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create new product"
        return context

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse(self.success_url)

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False


class ProductUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView
):
    model = Product
    form_class = ProductForm
    template_name = "product_create.html"
    success_url = "core:product"
    success_message = "%(product_name)s was updated successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit product"
        return context

    def get_success_url(self, **kwargs):
        return reverse(self.success_url)

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False


class ProductDeleteView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView
):
    model = Product
    template_name = "delete.html"
    success_url = "core:product"
    success_message = "%(name)s was deleted successfully"

    def get_success_url(self, **kwargs):
        return reverse(self.success_url)

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False


# ======================
# === Category Views ===
# ======================


class CategoryCreateView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView
):
    model = Category
    template_name = "category.html"
    form_class = CategoryForm
    success_url = "core:category"
    success_message = "%(name)s was created successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create new Category"
        context["categories"] = Category.objects.filter(status=True)
        return context

    def form_valid(self, form):
        form.instance.organization = self.request.user
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        return reverse(self.success_url)

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False


class CategoryUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView
):
    model = Category
    form_class = CategoryForm
    template_name = "category.html"
    success_url = "core:category"
    success_message = "%(name)s was updated successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit category"
        context["categories"] = Category.objects.filter(status=True)
        return context

    def get_success_url(self, **kwargs):
        return reverse(self.success_url)

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False


class CategoryDeleteView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView
):
    model = Category
    template_name = "delete.html"
    success_url = "core:category"
    success_message = "%(name)s was deleted successfully"

    def get_success_url(self, **kwargs):
        return reverse(self.success_url)

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False


# =========================
# === Subcategory Views ===
# =========================


class SubCategoryCreateView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView
):
    model = Subcategory
    template_name = "subcategory.html"
    form_class = SubcategoryForm
    success_url = "core:subcategory"
    success_message = "%(name)s was created successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add new sub-category"
        context["subcategories"] = Subcategory.objects.filter(status=True)
        return context

    def get_success_url(self, **kwargs):
        return reverse(self.success_url)

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False


class SubCategoryUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView
):
    model = Subcategory
    form_class = SubcategoryForm
    template_name = "subcategory.html"
    success_url = "core:subcategory"
    success_message = "%(name)s was updated successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit sub-category"
        context["subcategories"] = Subcategory.objects.filter(status=True)
        return context

    def get_success_url(self, **kwargs):
        return reverse(self.success_url)

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False


class SubCategoryDeleteView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView
):
    model = Subcategory
    template_name = "delete.html"
    success_url = "core:subcategory"
    success_message = "%(name)s was deleted successfully"

    def get_success_url(self, **kwargs):
        return reverse(self.success_url)

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False


# =======================
# === Warehouse Views ===
# =======================


class WarehouseCreateView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView
):
    model = Warehouse
    template_name = "warehouse.html"
    form_class = WarehouseForm
    success_url = "core:warehouse"
    success_message = "%(name)s was created successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["warehouses"] = Warehouse.objects.filter(status=True)
        context["title"] = "New Warehouse"
        return context

    def get_success_url(self, **kwargs):
        return reverse(self.success_url)

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False


class WarehouseUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView
):
    model = Warehouse
    template_name = "warehouse.html"
    form_class = WarehouseForm
    success_url = "core:warehouse"
    success_message = "%(name)s was Updated successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["warehouses"] = Warehouse.objects.filter(status=True)
        context["title"] = "Edit Warehouse"
        return context

    def get_success_url(self, **kwargs):
        return reverse(self.success_url)

    def test_func(self):
        if self.request.user.is_staff:
            return True
        return False


class WarehouseDeleteView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView
):
    model = Warehouse
    template_name = "delete.html"
    success_url = "core:warehouse"
    success_message = "%(name)s was deleted successfully"

    def get_success_url(self, **kwargs):
        return reverse(self.success_url)

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False


# >=========== update views =============>


# class ChalanUpdateView(LoginRequiredMixin,
#                         UserPassesTestMixin,
#                         SuccessMessageMixin,
#                         UpdateView):
#     model = Chalan
#     form_class = ChalanCreateForm
#     template_name = 'chalan/chalan_create.html'
#     success_url = 'core:chalan'
#     success_message = "%(name)s was updated successfully"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = 'Edit Chalan'
#         context["chalans"] = Chalan.objects.filter(status=True)
#         return context

#     def get_success_url(self, **kwargs):
#         return reverse(self.success_url)

#     def test_func(self):
#         if self.request.user.is_staff:
#             return True
#         return False


# >=================== delete views ===============>


# class ChalanDeleteView(LoginRequiredMixin,
#                     UserPassesTestMixin,
#                     SuccessMessageMixin,
#                     DeleteView):
#     model = Chalan
#     template_name = 'delete.html'
#     success_url = 'core:chalan'
#     success_message = "%(name)s was deleted successfully"

#     def get_success_url(self, **kwargs):
#         return reverse(self.success_url)

#     def test_func(self):
#         if self.request.user.is_superuser:
#             return True
#         return False
