from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
import logging

logger = logging.getLogger(__name__)

class Category(models.Model):
    title = models.CharField(max_length=200)
    sub_category = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        related_name='sub_categories', null=True, blank=True
    )
    is_sub = models.BooleanField(default=False)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    image = models.ImageField(upload_to='products')
    title = models.CharField(max_length=250)
    description = models.TextField()
    price = models.IntegerField()
    total_quantity = models.PositiveIntegerField(default=0)
    availability = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return self.slug

    def get_absolute_url(self):
        return reverse('shop:product_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def reduce_quantity(self, quantity):
        logger.debug(f"Current Quantity: {self.total_quantity}, Requested Quantity: {quantity}")
        if self.total_quantity >= quantity:
            self.total_quantity -= quantity
            logger.debug(f"New Quantity: {self.total_quantity}")
            if self.total_quantity == 0:
                self.availability = False
                logger.debug("Product marked as unavailable.")
            self.save()
        else:
            raise ValueError("Not enough stock available")
