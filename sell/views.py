from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
    View,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import Customer, SellProduct
from .forms import CustomerForm, SellProductForm
from core.models import User, Product


# ======================
# ===== Sale Views =====
# ======================


class SellProductListView(UserPassesTestMixin, LoginRequiredMixin, ListView):
    queryset = SellProduct.objects.filter(status=True)
    template_name = "sell/sales.html"
    paginate_by = "20"

    def test_func(self, *args, **kwargs):
        if self.request.user.is_staff:
            return True
        return False


class SellProductCreateView(
    UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, CreateView
):
    model = SellProduct
    template_name = "sell/product-create.html"
    form_class = SellProductForm
    success_url = "sell:sale-create"
    success_message = "%(product)s was successfully"

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        # update stock quatity
        product_instance = get_object_or_404(Product, id=form.instance.product.pk)
        product_instance.quantity -= form.instance.quantity

        product_instance.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "New Sale"
        return context

    def get_success_url(self, **kwargs):
        return reverse(self.success_url)

    def test_func(self, *args, **kwargs):
        if self.request.user.is_staff:
            return True
        return False


class SellProductUpdateView(
    UserPassesTestMixin, LoginRequiredMixin, SuccessMessageMixin, UpdateView
):
    model = SellProduct
    template_name = "sell/product-create.html"
    form_class = SellProductForm
    success_url = "sell:sales"
    success_message = "%(product)s was updated successfully"

    def form_valid(self, form):
        print()
        instance = get_object_or_404(SellProduct, id=form.instance.pk)
        stock_product = get_object_or_404(Product, id=instance.product.pk)
        quantity_before = int(instance.quantity)
        quantity_after = int(form.instance.quantity)

        # calculate updated quantity
        qty_diff = 0
        if quantity_before != quantity_after:
            qty_diff = quantity_before - quantity_after

        # # update stock quantity
        if qty_diff != 0:
            stock_product.quantity = stock_product.quantity + qty_diff

        # update stock
        stock_product.save()

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Edit Sale"
        return context

    def get_success_url(self, **kwargs):
        return reverse(self.success_url)

    def test_func(self, *args, **kwargs):
        if self.request.user.is_staff:
            return True
        return False


class SellProductDeleteView(SuccessMessageMixin, DeleteView):
    model = SellProduct
    template_name = "delete.html"
    success_url = "sell:sales"
    success_message = "%(name)s was deleted successfully"

    def get_success_url(self, **kwargs):
        return reverse(self.success_url)


# ======================
# === Customer Views ===
# ======================


class CustomerCreateView(SuccessMessageMixin, CreateView):
    model = Customer
    template_name = "sell/customer.html"
    form_class = CustomerForm
    success_url = "sell:customer"
    success_message = "%(name)s was created successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["customers"] = Customer.objects.filter(status=True)
        return context

    def get_success_url(self, **kwargs):
        return reverse(self.success_url)


class CustomerUpdateView(SuccessMessageMixin, UpdateView):
    model = Customer
    template_name = "sell/customer.html"
    form_class = CustomerForm
    success_url = "sell:customer"
    success_message = "%(name)s was updated successfully"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["customers"] = Customer.objects.filter(status=True)
        return context

    def get_success_url(self, **kwargs):
        return reverse(self.success_url)


class CustomerDeleteView(SuccessMessageMixin, DeleteView):
    model = Customer
    template_name = "delete.html"
    success_url = "sell:customer"
    success_message = "%(name)s was deleted successfully"

    def get_success_url(self, **kwargs):
        return reverse(self.success_url)


class SingleCustomerView(View):
    def get(self, request, pk):
        customer = get_object_or_404(Customer, pk=pk)
        sellproduct = Customer.objects.filter(id=customer.id)
        context = {"customer": customer, "sellproduct": sellproduct}
        return render(self.request, "sell/single-customer.html", context)
