from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse
from core.models import Product, User

from datetime import date


class PurchaseProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    remark = models.TextField(blank=True, null=True, max_length=254)

    added_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    status = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.product_name

    @property
    def purchase_no(self):
        product = str(self.product.product_name)
        d = date.today()
        d = d.strftime("%d%m%y")
        return (product[:3] + str(self.id) + "-" + d).upper()

    @property
    def total_price(self):
        return self.price * self.quantity

    def get_update_url(self):
        return reverse("purchase:purchase-edit", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("purchase:purchase-delete", kwargs={"pk": self.pk})

    def get_invoice_url(self):
        return reverse("purchase:purchase-invoice", kwargs={"pk": self.pk})
