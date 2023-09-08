from django.contrib import admin
from menu.models import Meal, Comment


class MealAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "in_menu")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("meal_id", "user_id", "description")


# Register your models here.
admin.site.register(Meal, MealAdmin)
admin.site.register(Comment, CommentAdmin)
