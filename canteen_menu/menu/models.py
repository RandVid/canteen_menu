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
    user_id = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return f"{self.meal_id}  {self.user_id}"
