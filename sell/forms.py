from django import forms
from django.forms.models import inlineformset_factory
from .models import Customer, SellProduct


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["name", "email", "phone"]


class SellProductForm(forms.ModelForm):
    class Meta:
        model = SellProduct
        fields = [
            "customer",
            "product",
            "quantity",
            "price",
            # "added_by",
        ]
