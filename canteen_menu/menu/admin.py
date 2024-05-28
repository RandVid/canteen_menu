from django.contrib import admin
from menu.models import Meal, Comment, FavoriteMeal, MealCategory


class MealAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "in_menu")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("meal_id", "username", "description")


class FavoriteMealAdmin(admin.ModelAdmin):
    list_display = ("username", "meal_id")


class MealCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "id")


# Register your models here.
admin.site.register(Meal, MealAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(FavoriteMeal, FavoriteMealAdmin)
admin.site.register(MealCategory, MealCategoryAdmin)
