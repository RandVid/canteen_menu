from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from menu.models import Meal


# Create your views here.
def main(request):
    meals = Meal.objects.filter(in_menu=True).values()
    template = loader.get_template('main.html')
    context = {
        'meals': meals,
    }
    return HttpResponse(template.render(context, request))


def details(request, id):
    meal = Meal.objects.get(id=id)
    template = loader.get_template('details.html')
    context = {
        'meal': meal,
    }
    return HttpResponse(template.render(context, request))
