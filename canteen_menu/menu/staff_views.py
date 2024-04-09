from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.template import loader

from .models import Meal, MealCategory
from .forms import MealForm, CategoryForm


def update_menu(request, meal_id):
    if request.method == 'POST' and request.user.is_staff:
        meal = get_object_or_404(Meal, id=meal_id)
        meal.in_menu = not meal.in_menu
        meal.save()
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


def delete_meal(request, meal_id):
    if request.method == 'POST' and request.user.is_staff:
        meal = get_object_or_404(Meal, id=meal_id)
        meal.delete()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})


def add_meal(request):
    if request.user.is_staff:
        if request.method == "POST":
            form = MealForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("staff")
            messages.error(request, "Unsuccessful operation.")
        form = MealForm()
        template = loader.get_template('update_meal.html')
        context = {
            'form': form
        }
        return HttpResponse(template.render(context, request))
    else:
        messages.error(request, "Unsuccessful operation. User has no rights")
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


def staff_categories(request):
    categories = MealCategory.objects.all().values()
    template = loader.get_template('staff_categories.html')
    context = {
        'categories': categories
    }
    return HttpResponse(template.render(context, request))


def delete_category(request, category_id):
    if request.method == 'POST' and request.user.is_staff:
        category = get_object_or_404(MealCategory, id=category_id)
        category.delete()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})


def add_category(request):
    if request.user.is_staff:
        if request.method == "POST":
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("staff/categories/")
            messages.error(request, "Unsuccessful operation.")
        form = CategoryForm()
        template = loader.get_template('update_category.html')
        context = {
            'form': form
        }
        return HttpResponse(template.render(context, request))
    else:
        messages.error(request, "Unsuccessful operation. User has no rights")
        return JsonResponse({'status': 'error'})


def update_category(request, category_id):
    category = MealCategory.objects.get(id=category_id)
    if request.user.is_staff:
        if request.method == "POST":
            form = CategoryForm(request.POST, instance=category)
            if form.is_valid():
                form.save()
                return redirect("/staff/categories/")
            messages.error(request, "Unsuccessful registration. Invalid information.")
        form = CategoryForm(instance=category)
        template = loader.get_template('update_meal.html')
        context = {
            'form': form
        }
        return HttpResponse(template.render(context, request))
    else:
        return JsonResponse({'status': 'error'})
