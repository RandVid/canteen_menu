from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('details/<int:id>', views.details, name='details'),
    path('favorite/update/<int:meal_id>/', views.update_favorite),
    path('favorite', views.favorite_meals)
]
