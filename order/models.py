from django.db import models
from core.models import Product, User
from django.urls import reverse


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    order_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product)

    @property
    def total_item_price(self):
        return self.product.sell_price * self.quantity

    def get_update_url(self):
        return reverse("order:order-edit", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse("order:order-delete", kwargs={"pk": self.pk})
