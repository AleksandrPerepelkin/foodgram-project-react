from collections import defaultdict

from django.db.models import Sum

from recipes.models import IngredientRecipe


def download_ingredients(user):
    """Метод для формирования списка покупок"""
    ingredients = defaultdict(int)

    ingredient_recipes = IngredientRecipe.objects.filter(
        recipe__recipe_cart__user=user,
    ).values(
        'ingredient__name',
        'ingredient__measurement_unit',
    ).annotate(
        total_amount=Sum('amount'),
    )

    ingredients_to_file = 'Список покупок:\n'
    count = 1

    for ingredient in ingredient_recipes:
        name = ingredient['ingredient__name']
        measurement_unit = ingredient['ingredient__measurement_unit']
        total_amount = ingredient['total_amount']
        ingredient_str = f'{name}, {measurement_unit}'
        ingredients[ingredient_str] = total_amount

    for key, value in ingredients.items():
        ingredients_to_file += f'{count}. {key} - {value}\n'
        count += 1

    ingredients_to_file += '\n\n Foodgram ©'

    return ingredients_to_file
