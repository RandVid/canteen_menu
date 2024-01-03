from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('details/<int:id>', views.details, name='details'),
    path('favorite/update/<int:meal_id>/', views.update_favorite),
    path('favorite', views.favorite_meals),
    path('staff', views.staff_meals, name='staff'),
    path('staff/menu/update/<int:meal_id>/', views.update_menu),
    path('staff/meal/add/', views.add_meal),
    path('staff/meal/update/<int:meal_id>/', views.update_meal),
    path('staff/meal/delete/<int:meal_id>/', views.delete_meal)
]
