from django.urls import reverse
from distutils.command.upload import upload
from tabnanny import verbose
from unicodedata import category
from django.db import models


class Category(models.Model):
    category_name= models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)
    description = models.CharField(max_length=255, blank=True)
    cat_image = models.ImageField(upload_to = 'photos/categories/', blank=True)

    class Meta:
        verbose_name_plural='categories'
    
    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    def __str__(self):
        return self.category_name
    