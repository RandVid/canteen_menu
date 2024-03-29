from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader

from menu.models import Meal, Comment, FavoriteMeal
from .forms import CommentForm


# Create your views here.
def main(request):
    meals = Meal.objects.filter(in_menu=True).values()
    favorite = list(FavoriteMeal.objects.filter(username=request.user).values_list('meal_id', flat=True))
    print(favorite)
    template = loader.get_template('main.html')
    context = {
        'meals': meals,
        'favorite_meals': favorite
    }
    return HttpResponse(template.render(context, request))


def details(request, id):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            new_comment = form.save(commit=False)
            new_comment.username = request.user
            new_comment.meal_id = id
            comments = Comment.objects.filter(meal_id=id, username=new_comment.username)
            comments.delete()
            new_comment.save()

    meal = Meal.objects.get(id=id)
    comments = Comment.objects.filter(meal_id=id).values()
    template = loader.get_template('details.html')
    form = CommentForm()
    context = {
        'meal': meal,
        'comments': comments,
        'form': form
    }
    return HttpResponse(template.render(context, request))


def favorite_meals(request):
    favorite = list(FavoriteMeal.objects.filter(username=request.user).values_list('meal_id', flat=True))
    in_menu = Meal.objects.filter(in_menu=True, id__in=favorite).values()
    not_in_menu = Meal.objects.filter(in_menu=False, id__in=favorite).values()
    template = loader.get_template('favorite_meals.html')
    context = {
        'favorite_meals': favorite,
        'favorite_in_menu': in_menu,
        'favorite_not_in_menu': not_in_menu
    }
    return HttpResponse(template.render(context, request))


def update_favorite(request, meal_id):
    if request.method == 'POST':
        favorite_meal = FavoriteMeal.objects.filter(meal_id=meal_id, username=request.user)
        if favorite_meal:
            favorite_meal.delete()
        else:
            favorite_meal = FavoriteMeal(meal_id=meal_id, username=request.user)
            favorite_meal.save()
        print(FavoriteMeal.objects.all().values())
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})
