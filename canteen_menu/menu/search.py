from django.db.models import When, Value, IntegerField, Case, Q
from unidecode import unidecode

from .models import MealCategory


def meal_search(meal_set, query):
    names = list(meal_set.values_list('name', flat=True))
    good_names = [name for name in names if unidecode(query.lower()) in unidecode(name.lower())]
    suited_meal_list = meal_set.filter(name__in=good_names)
    return suited_meal_list


def levenshtein_distance(query, string):
    ql, sl = len(query), len(string)
    dp = [[0] * (sl + 1) for _ in range(ql + 1)]

    for i in range(1, ql + 1):
        for j in range(1, sl + 1):
            if query[i - 1] == string[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j],  # deletion
                                   dp[i][j - 1],  # insertion
                                   dp[i - 1][j - 1])  # substitution

    return dp[ql][sl]


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
