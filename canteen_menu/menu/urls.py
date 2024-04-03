from django.urls import path
from .views import *
from .staff_views import *

urlpatterns = [
    path('', main, name='main'),
    path('details/<int:id>', details, name='details'),
    path('comment/delete/<int:comment_id>', delete_comment),
    path('favorite/update/<int:meal_id>/', update_favorite),
    path('favorite', favorite_meals),
    path('staff', staff_meals, name='staff'),
    path('staff/menu/update/<int:meal_id>/', update_menu),
    path('staff/meal/add/', add_meal),
    path('staff/meal/update/<int:meal_id>/', update_meal),
    path('staff/meal/delete/<int:meal_id>/', delete_meal),
    path('staff/categories/', staff_categories),
    path('staff/categories/add/', add_category),
    # path('staff/categories/update/<int:meal_id>/', update_category),
    path('staff/categories/delete/<int:category_id>/', delete_category),
]
