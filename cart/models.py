from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from shop.models import Product


class Cart(models.Model):
    owner = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.owner}'s"


class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, related_name='products', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_products', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    now_in_cart = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created']
        indexes = [models.Index(fields=['-created'])]

    def __str__(self):
        return self.product.name

    def get_absolute_url(self):
        return reverse('cart:cart_detail', args=[self.id, self.product.slug])
