from dataclasses import field
from pyexpat import model
from django import forms
from .models import Order


class OredrForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'email', 'wilaya', 'address', 'order_note' ]