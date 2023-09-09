from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class ProductCategory(models.Model):
    name = models.CharField(_('Category name'), max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Product Category')
        verbose_name_plural = _('Product Categories')

    def __str__(self):
        return self.name


def get_default_product_category():
    return ProductCategory.objects.get_or_create(name='Others')[0]


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, related_name="product_list", on_delete=models.SET(get_default_product_category))
    name = models.CharField(max_length=200)
    desc = models.TextField(_('Description'), blank=True)
    image = models.ImageField(upload_to="products/", blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    quantity = models.IntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at', )

    def __str__(self):
        return self.name