from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from restaurant.models import Dish, Cook, Ingredient, DishType


# Create your views here.

@login_required
def index(request):
    num_dishes = Dish.objects.count()
    num_cooks = Cook.objects.count()
    num_dishtype = DishType.objects.count()
    num_ingredients = Ingredient.objects.count()

    context = {
        "num_dishes": num_dishes,
        "num_cooks": num_cooks,
        "num_dishtype": num_dishtype,
        "num_ingredients": num_ingredients
    }

    return render(
        request,
        "restaurant/index.html",
        context=context
    )