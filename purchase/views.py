from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
    TemplateView,
    View,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import *
from .forms import *

from core.models import Product, Organization, Warehouse
from core.forms import CategoryForm, WarehouseForm, SubcategoryForm

import json
from datetime import date
from django.template.loader import get_template
from xhtml2pdf import pisa


def purchaes_invoice(request, *args, **kwargs):
    pk = kwargs.get("pk")
    purchase = get_object_or_404(PurchaseProduct, pk=pk)

    template_path = "purchase/invoice.html"
    context = {"purchase": purchase}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type="application/pdf")
    # if we want to download the pdf :
    # response['Content-Disposition'] = 'attachment; filename="report.pdf"'
    # if we want to display the pdf :
    filename = f"invoice{pk}-{date.today()}"
    response["Content-Disposition"] = f'filename="{filename}.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse("We had some errors <pre>" + html + "</pre>")
    return response


class PurchaseProductList(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, TemplateView
):
    template_name = "purchase/product.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = PurchaseProduct.objects.filter(status=True)
        return context

    def test_func(self, *args, **kwargs):
        if self.request.user.is_staff:
            return True
        return False


class CreatePurchaseView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, View
):
    def get(self, *args, **kwargs):
        form = PurchaseProductForm()
        context = {
            "form": form,
            "title": "Create New Purchase",
            "warehouse_form": WarehouseForm(),
            "category_form": CategoryForm(),
            "subcategory_form": SubcategoryForm(),
        }
        return render(self.request, "purchase/product-create.html", context)

    def post(self, *args, **kwargs):
        form = PurchaseProductForm(self.request.POST or None)

        if form.is_valid():
            product = form.cleaned_data.get("product")
            quantity = form.cleaned_data.get("quantity")

            product_instance = get_object_or_404(Product, id=product.id)
            product_instance.quantity += quantity

            new_purchase = form.save(commit=False)
            new_purchase.added_by = self.request.user
            new_purchase.save()
            product_instance.save()

            messages.success(self.request, "Item was purchased successfully")
            return redirect("purchase:purchase-create")
        else:
            messages.warning(self.request, "Invalid form value. Please try again")
            return redirect("purchase:purchase-create")

    def test_func(self, *args, **kwargs):
        if self.request.user.is_staff:
            return True
        return False


class PurchaseProductDetailView(DetailView):
    model = PurchaseProduct
    template_name = "purchase-detali.html"


class PurchaseProductUpdateView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView
):
    model = PurchaseProduct
    form_class = PurchaseProductForm
    template_name = "purchase/product-create.html"
    success_url = "./"
    success_message = "%(name)s was updated successfully"

    def post(self, request, pk, *args, **kwargs):
        instance = PurchaseProduct.objects.get(pk=pk)
        stock_product = Product.objects.get(pk=instance.product.pk)
        form = PurchaseProductForm(self.request.POST or None, instance=instance)

        quantity_before = int(instance.quantity)

        if form.is_valid():
            quantity_after = int(form.cleaned_data.get("quantity"))

            # calculate updated quantity
            qty_diff = 0
            if quantity_before != quantity_after:
                qty_diff = quantity_before - quantity_after

            # update stock quantity
            if qty_diff != 0:
                stock_product.quantity = stock_product.quantity + qty_diff

            # save form
            form.save()
            # update stock
            stock_product.save()

            messages.success(self.request, "Item was updated successfully")
            return redirect("./")
        else:
            messages.warning(self.request, "Invalid form value. Please try again")
            return redirect("./")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = PurchaseProduct.objects.filter(status=True)
        context["title"] = "Edit Purchase"
        return context

    def get_success_url(self, **kwargs):
        return reverse(self.success_url)

    def test_func(self, *args, **kwargs):
        if self.request.user.is_staff:
            return True
        return False


class PurchaseProductDeleteView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, DeleteView
):
    model = PurchaseProduct
    template_name = "delete.html"
    success_url = "purchase:product"
    success_message = "%(name)s was created successfully"

    def get_success_url(self, **kwargs):
        return reverse(self.success_url)

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        return False
