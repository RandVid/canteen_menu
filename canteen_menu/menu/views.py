from django.middleware.csrf import get_token
from django.http import HttpResponse, JsonResponse
from django.template import loader

from .models import Meal, Comment, FavoriteMeal, MealCategory
from .forms import CommentForm
from .search import meal_sort, meal_search, typo_tolerant_search


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


def delete_comment(request, comment_id):
    print('aboba')
    if request.method == 'POST':
        comment = Comment.objects.filter(id=comment_id).first()
        print(comment)
        if request.user.username == comment.username or request.user.is_superuser:
            comment.delete()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})
