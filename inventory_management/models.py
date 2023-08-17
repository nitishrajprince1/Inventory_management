from datetime import datetime

from django.contrib.auth.models import User
from django.db import models

STATUS_CHOICES = (
    ("Change Pending", "Change Pending"),
    ("Delete Pending", "Delete Pending"),
    ("Pending", "Pending"),
    ("Approved", "Approved"),
)
ROLE_CHOICES = (
    ("Department Manager,", "Department Manager"),
    ("Store Manager", "Store Manager"),
)


class Role(models.Model):
    name = models.CharField(max_length=50, choices=ROLE_CHOICES, default="Pending")

    def __str__(self):
        return "{}".format(self.name)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roles = models.ManyToManyField(Role)

    def __str__(self):
        return "{}".format(self.user.username)


class Inventory(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=200)
    vendor = models.CharField(max_length=200)
    mrp = models.DecimalField(max_digits=10, decimal_places=2)
    batch_num = models.PositiveIntegerField()
    batch_date = models.DateField(default=datetime.now)
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Pending")

    class Meta:
        verbose_name_plural = "Inventories"

    def __str__(self):
        return "{}".format(self.product_name)
