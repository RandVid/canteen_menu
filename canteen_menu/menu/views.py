from django.contrib import messages
from django.db.models import Value, IntegerField, F, When, Case, Q
from django.middleware.csrf import get_token
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template import loader

from .models import Meal, Comment, FavoriteMeal, MealCategory
from .forms import CommentForm, MealForm
from .templatetags.custom_filters import get_category_name

from unidecode import unidecode


# Create your views here.
def main(request):
    meals = Meal.objects.filter(in_menu=True).values()
    favorite = list(FavoriteMeal.objects.filter(username=request.user).values_list('meal_id', flat=True))
    categories = MealCategory.objects.all().values()
    if request.method == "POST":
        input_value = request.POST.get('input-value')
        meals = meal_sort(request, meals, categories=categories)
        possible_meals_html = ''
        is_authenticated = request.user.is_authenticated
        if len(input_value) > 1:
            # print(typo_tolerant_search(input_value, meals, tolerance=len(input_value) - 1))
            possible_meals = typo_tolerant_search(input_value, meals, tolerance=len(input_value) - 1)
            if len(possible_meals) > 0:
                possible_meals_html = '<h2 style="text-align: center;"> Galima jūs ieškote </h2>\n'
                possible_meals_html += loader.render_to_string('meals.html', {'meals': possible_meals,
                                                                              'is_authenticated': is_authenticated,
                                                                              'favorite_meals': favorite,
                                                                              'csrf_token': get_token(request)})
            # print(possible_meals_html)
        meals = meal_search(meals, input_value)
        meals_html = loader.render_to_string('meals.html', {'meals': meals,
                                                            'is_authenticated': is_authenticated,
                                                            'favorite_meals': favorite,
                                                            'csrf_token': get_token(request)})
        return JsonResponse({'status': 'success', 'meals1': meals_html, 'meals2': possible_meals_html})

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
    meals = Meal.objects.filter(id__in=favorite)
    template = loader.get_template('favorite_meals.html')
    categories = MealCategory.objects.all().values()

    if request.method == "POST":
        meals = meal_sort(request, meals, categories=categories)
        is_authenticated = request.user.is_authenticated
            # print(possible_meals_html)
        input_value = request.POST.get('input-value')
        meals = meal_search(meals, input_value)
        in_menu = meals.filter(in_menu=True)
        not_in_menu = meals.filter(in_menu=False)

        in_menu_html = loader.render_to_string('meals.html', {'meals': in_menu,
                                                            'is_authenticated': is_authenticated,
                                                            'favorite_meals': favorite,
                                                            'csrf_token': get_token(request)})
        not_in_menu_html = loader.render_to_string('meals.html', {'meals': not_in_menu,
                                                              'is_authenticated': is_authenticated,
                                                              'favorite_meals': favorite,
                                                              'csrf_token': get_token(request)})
        return JsonResponse({'status': 'success', 'meals1': in_menu_html, 'meals2': not_in_menu_html})

    in_menu = Meal.objects.filter(in_menu=True, id__in=favorite).values()
    not_in_menu = Meal.objects.filter(in_menu=False, id__in=favorite).values()
    context = {
        'favorite_meals': favorite,
        'favorite_in_menu': in_menu,
        'favorite_not_in_menu': not_in_menu,
        'categories': categories
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
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})


def update_menu(request, meal_id):
    if request.method == 'POST' and request.user.is_staff:
        meal = get_object_or_404(Meal, id=meal_id)
        meal.in_menu = not meal.in_menu
        meal.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})


def delete_meal(request, meal_id):
    if request.method == 'POST' and request.user.is_staff:
        meal = get_object_or_404(Meal, id=meal_id)
        meal.delete()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})


def staff_meals(request):
    meals = Meal.objects.all().values()
    template = loader.get_template('staff_meals.html')
    context = {
        'meals': meals
    }
    return HttpResponse(template.render(context, request))


def add_meal(request):
    if request.user.is_staff:
        if request.method == "POST":
            form = MealForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("staff")
            messages.error(request, "Unsuccessful registration. Invalid information.")
        form = MealForm()
        template = loader.get_template('update_meal.html')
        context = {
            'form': form
        }
        return HttpResponse(template.render(context, request))
    else:
        return JsonResponse({'status': 'error'})


def update_meal(request, meal_id):
    meal = Meal.objects.get(id=meal_id)
    if request.user.is_staff:
        if request.method == "POST":
            form = MealForm(request.POST, instance=meal)
            if form.is_valid():
                form.save()
                return redirect("staff")
            messages.error(request, "Unsuccessful registration. Invalid information.")
        form = MealForm(instance=meal)
        template = loader.get_template('update_meal.html')
        context = {
            'form': form
        }
        return HttpResponse(template.render(context, request))
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
                dp[i][j] = 1 + min(dp[i - 1][j],  # deletion
                                   dp[i][j - 1],  # insertion
                                   dp[i - 1][j - 1])  # substitution

    return dp[m][n]


def typo_tolerant_search(query, meal_set, tolerance=2):
    results = []
    names = list(meal_set.values_list('name', flat=True))

    for name in names:
        if unidecode(query.lower()) not in unidecode(name.lower()):
            distance = (levenshtein_distance(unidecode(query.lower()), unidecode(name.lower()))
                        - len(name) + len(query))
            if distance <= tolerance:
                results.append((name, distance))
    names_results = [i[0] for i in results]
    case_statements = [When(name=name, then=Value(distance, output_field=IntegerField())) for name, distance in results]
    meal_set = meal_set.filter(name__in=names_results).annotate(
        distance=Case(*case_statements, default=Value(0, output_field=IntegerField()))
    )
    print(meal_set.values_list('distance', flat=True))
    # results.sort(key=lambda x: x[1])  # Sort results by distance
    # print(results)
    meal_set = meal_set.order_by('distance')
    print(meal_set)
    return meal_set


def meal_sort(request, meal_set, categories=MealCategory.objects.all().values()):
    chosen_categories = [c['name'] for c in categories if request.POST.get('C-' + c['name'])]
    if request.POST.get('only-vegan'):
        meal_set = meal_set.filter(is_vegan=True)
    meal_set = meal_set.filter(category_id__in=chosen_categories)
    meal_set = meal_set.filter(Q(calories__gte=request.POST.get('cal-min'), calories__lte=request.POST.get('cal-max')) |
                               Q(calories=None))
    # print(meal_set)
    return meal_set
