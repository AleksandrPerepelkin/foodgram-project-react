from collections import defaultdict

from recipes.models import IngredientRecipe


def download_ingredients(user):

    """Метод для формирования списка покупок."""

    ingredients = defaultdict(int)
    ingredient_recipes = IngredientRecipe.objects.filter(
        recipe__recipe_cart__user=user).values(
        'ingredient__name',
        'ingredient__measurement_unit').annotate(
        amount='result')

    for ingredient_recipe in ingredient_recipes:
        name = ingredient_recipe['ingredient__name']
        measurement_unit = ingredient_recipe['ingredient__measurement_unit']
        ingredient = f'{name}, {measurement_unit}'
        result = ingredient_recipe['result']
        ingredients[ingredient] += result
    ingredients_to_file = 'Список покупок:\n'
    count = 1

    for key, value in ingredients.items():
        ingredients_to_file += f'{count}. {key} - {value}\n'
        count += 1

    ingredients_to_file += '\n\n Foodgram ©'

    return ingredients_to_file
