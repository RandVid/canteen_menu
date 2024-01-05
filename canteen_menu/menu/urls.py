from django.urls import path
from .views import *
from .staff_views import *

urlpatterns = [
    path('', main, name='main'),
    path('details/<int:id>', details, name='details'),
    path('favorite/update/<int:meal_id>/', update_favorite),
    path('favorite', favorite_meals),
    path('staff', staff_meals, name='staff'),
    path('staff/menu/update/<int:meal_id>/', update_menu),
    path('staff/meal/add/', add_meal),
    path('staff/meal/update/<int:meal_id>/', update_meal),
    path('staff/meal/delete/<int:meal_id>/', delete_meal)
]
