from django.db import models
from django.contrib import settings
import stripe

# Create your models here.


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, null=False)
    description = models.TextField(null=False)
    image = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    stock = models.IntegerField(default=0)
    stripe_product_id = models.CharField(max_length=100, null=True)
    stripe_price_id = models.CharField(max_length=100, null=True)
    
    def save(self, *args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe_product = stripe.Product.create(name=self.title)
        stripe_price = stripe.Product.create(
            currency='inr', product=stripe_product.id, unit_amount=int(self.price * 100))
        self.stripe_product_id = stripe_product.id
        self.stripe_price_id = stripe_price.id
        return super().save(*args, **kwargs)