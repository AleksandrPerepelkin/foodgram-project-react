# Миксин для операций с корзиной
from recipes.models import Recipe, Favorite
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from .serializers import RecipeSmallSerializer
from shopping_cart.models import ShoppingCart


class ShoppingCartMixin:

    def add_to_cart(self, recipe_id, quantity):
        cart = get_object_or_404(Recipe, pk=self.kwargs['pk'])
        try:
            recipe = Recipe.objects.get(pk=recipe_id)
        except Recipe.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        recipe_in_cart = ShoppingCart(cart=cart, recipe=recipe,
                                      quantity=quantity,
                                      user=self.request.user)
        recipe_in_cart.save()
        serializer = RecipeSmallSerializer(recipe_in_cart)
        return serializer.data, status.HTTP_201_CREATED

    def remove_from_cart(self, recipe_id):
        recipe_in_cart = ShoppingCart.objects.filter(user=self.request.user,
                                                     recipe=recipe_id)
        if recipe_in_cart.exists():
            recipe_in_cart.delete()
            return {
                'message': 'Рецепт успешно удален из корзины',
                }, status.HTTP_204_NO_CONTENT
        return {'message': 'Рецепта не было в корзине'}
    status.HTTP_400_BAD_REQUEST


# Миксин для операций с избранным
class FavoriteMixin:

    def add_to_favorite(self, recipe_id):
        recipe = get_object_or_404(Recipe, id=recipe_id)
        if Favorite.objects.filter(user=self.request.user,
                                   recipe=recipe).exists():
            return {
                'error': 'Вы уже добавили этот рецепт в избранное',
                }, status.HTTP_400_BAD_REQUEST
        favorite_recipe = Favorite.objects.create(user=self.request.user,
                                                  recipe=recipe)
        serializer = RecipeSmallSerializer(favorite_recipe.recipe)
        return serializer.data, status.HTTP_201_CREATED

    def remove_from_favorite(self, recipe_id):
        favorite_recipe = Favorite.objects.filter(user=self.request.user,
                                                  recipe=recipe_id)
        if favorite_recipe.exists():
            favorite_recipe.delete()
            return {
                'message': 'Рецепт успешно удален из избранного',
                }, status.HTTP_204_NO_CONTENT
        return {
            'message': 'Рецепта не было в избранном',
            }, status.HTTP_400_BAD_REQUEST
