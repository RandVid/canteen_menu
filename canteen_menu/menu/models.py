from django.db import models


# Create your models here.
class Meal(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    price = models.FloatField()
    in_menu = models.BooleanField()

    def __str__(self):
        return f"{self.name}"


class Comment(models.Model):
    meal_id = models.IntegerField()
    username = models.CharField(max_length=150)
    description = models.TextField(null=True)
    rating = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.meal_id}  {self.username}"


class FavoriteMeal(models.Model):
    meal_id = models.IntegerField()
    username = models.CharField(max_length=150)
