from django.db import models


class MealCategory(models.Model):
    name = models.CharField(max_length=150, unique="True")

    def __str__(self):
        return self.name


# Create your models here.
class Meal(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField()
    in_menu = models.BooleanField()
    is_vegan = models.BooleanField()
    calories = models.IntegerField(null=True, blank=True)
    proteins = models.IntegerField(null=True, blank=True)
    fats = models.IntegerField(null=True, blank=True)
    carbohydrates = models.IntegerField(null=True, blank=True)
    mass = models.IntegerField(null=True, blank=True)
    category = models.ForeignKey(MealCategory, on_delete=models.CASCADE, to_field="name", null=True)

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
