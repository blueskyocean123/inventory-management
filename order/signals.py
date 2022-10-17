from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Order
from sell.models import Customer


@receiver(post_save, sender=Order)
def add_customer(sender, instance, created, **kwargs):
    customer_phone = instance.user.phone
    customer = Customer.objects.filter(phone=customer_phone)
    if created:
        if not customer:
            Customer.objects.create(
                name = instance.user.username,
                email = instance.user.email,
                phone = instance.user.phone,
            )
        print('done')