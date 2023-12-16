from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader

from .models import Meal, Comment, FavoriteMeal, MealCategory
from .forms import CommentForm
from .templatetags.custom_filters import get_category_name

from unidecode import unidecode


# Create your views here.
def main(request):
    meals = Meal.objects.filter(in_menu=True).values()
    if request.method == "POST":
        input_value = request.POST.get('input_value')
        meals = meal_search(meals, input_value)
    favorite = list(FavoriteMeal.objects.filter(username=request.user).values_list('meal_id', flat=True))
    categories = MealCategory.objects.all().values()
    # print(meals[0]["category_id"])
    print(get_category_name(categories, meals[1]["category_id"]))
    template = loader.get_template('main.html')
    context = {
        'meals': meals,
        'favorite_meals': favorite,
        'categories': categories
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


def meal_search(meal_set, query):
    names = list(meal_set.values_list('name', flat=True))
    good_names = accent_insensitive_search(names, query)
    suited_meal_list = meal_set.filter(name__in=good_names)
    return suited_meal_list


def accent_insensitive_search(names, query):
    good_names = [name for name in names if unidecode(query.lower()) in unidecode(name.lower())]
    return good_names


def levenshtein_distance(str1, str2):
    m, n = len(str1), len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j],      # deletion
                                  dp[i][j - 1],      # insertion
                                  dp[i - 1][j - 1])  # substitution

    return dp[m][n]


def typo_tolerant_search(query, word_list, tolerance=2):
    results = []

    for word in word_list:
        distance = levenshtein_distance(unidecode(query.lower()), unidecode(word.lower())) - len(word) + len(query)
        if distance <= tolerance:
            results.append((word, distance))

    results.sort(key=lambda x: x[1])  # Sort results by distance
    return results
