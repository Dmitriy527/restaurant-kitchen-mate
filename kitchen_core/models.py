from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class DishType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Cook(AbstractUser):
    years_of_experience = models.IntegerField(default=0)

    class Meta:
        verbose_name = "cook"
        verbose_name_plural = "cooks"
        ordering = ["username"]

    def get_absolute_url(self):
        return reverse("kitchen_core:cooks-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.username} {self.first_name} {self.last_name}"


class Dish(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=9, decimal_places=2)

    dish_type = models.ForeignKey(
        DishType,
        on_delete=models.CASCADE,
        related_name="dishes",
    )
    cooks = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="dishes"
    )

    def __str__(self):
        return f"{self.name} (price: {self.price}, dish type:  {self.dish_type})"
