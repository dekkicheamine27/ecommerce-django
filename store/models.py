from django.db import models
from django.urls import reverse
from category.models import Category

# Create your models here.

class Product(models.Model):
    product_name  = models.CharField(max_length=255)
    slug          = models.SlugField(max_length=255, blank=True)
    description   = models.CharField(max_length=255, blank=True)
    price         = models.DecimalField(max_digits=6, decimal_places=2)
    images        = models.ImageField(upload_to = 'photos/products/', blank=True)
    stock         = models.IntegerField()
    is_available  = models.BooleanField(default=True)
    category      = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date  = models.DateField(auto_now_add=True)
    modified_date  = models.DateField(auto_now =True)

    def __str__(self):
        return self.product_name

    def get_product_url(self):
        return reverse('product_detail', args=[self.category.slug ,self.slug])
    


