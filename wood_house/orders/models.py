from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from wood_house.products.models import Product


class Order(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("completed", "completed"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Recalculate total after saving
        self.recalculate_total()

    def recalculate_total(self):
        """
        Recalculate order total based on related order items
        """
        total = sum(item.get_item_total() for item in self.orderitem_set.all())
        if self.total != total:
            self.total = total
            self.save()

    def __str__(self):
        return f"Order{self.id} - {self.user.username} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(
        validators=[
            MinValueValidator(1, message="Quantity must be at least 1"),
            MaxValueValidator(100, message="Quantity cannot exceed 100"),
        ]
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        # Set Price from product if not already set
        if not self.price:
            self.price = self.product.price
        super().save(*args, **kwargs)
        # Update order total
        self.order.recalculate_total()

    def get_item_total(self):
        """
        Calculate total price for this item
        """
        return self.quantity * self.price

    def __str__(self):
        return f"{self.quantity}x {self.product.name} in Order {self.order.id}"

    class Meta:
        indexes = [models.Index(fields=["order"]), models.Index(fields=["product"])]
