"""Миксин для операций с корзиной."""
from django.shortcuts import get_object_or_404
from rest_framework import status

from recipes.models import Favorite
from shopping_cart.models import ShoppingCart
from .serializers import RecipeSmallSerializer


class ItemManagementMixin:

    def add_to_list(self,
                    request,
                    model_class,
                    model_name,
                    item_id,
                    error_message,
                    success_status):
        try:
            item = model_class.objects.get(pk=item_id)
        except model_class.DoesNotExist:
            return {'error': error_message}, status.HTTP_404_NOT_FOUND

        if model_class.objects.filter(user=request.user,
                                      **{model_name: item}).exists():
            return {'error': 'Вы уже добавили этот рецепт в избранное'}
        status.HTTP_400_BAD_REQUEST

        list_item = model_class.objects.create(user=request.user,
                                               **{model_name: item})
        serializer = RecipeSmallSerializer(list_item.recipe)
        return serializer.data, success_status

    def add_to_cart(self, request, recipe_id):
        return self.add_to_list(request,
                                ShoppingCart,
                                'recipe',
                                recipe_id,
                                'Рецепт не найден',
                                status.HTTP_201_CREATED)

    def add_to_favorite(self, request, recipe_id):
        return self.add_to_list(request,
                                Favorite,
                                'recipe',
                                recipe_id,
                                'Рецепт не найден',
                                status.HTTP_201_CREATED)

    def remove_item(self,
                    model_class,
                    model_name,
                    item_id,
                    success_message):
        item = model_class.objects.filter(user=self.request.user,
                                          **{model_name: item_id})
        if item.exists():
            item.delete()
            return {'message': success_message}, status.HTTP_204_NO_CONTENT
        return {'message': f'{model_name.capitalize()} не было в избранном'}
    status.HTTP_400_BAD_REQUEST

    def remove_from_cart(self, recipe_id):
        return self.remove_item(ShoppingCart,
                                'recipe',
                                recipe_id,
                                'Рецепт успешно удален из корзины')

    def remove_from_favorite(self, recipe_id):
        return self.remove_item(Favorite,
                                'recipe',
                                recipe_id,
                                'Рецепт успешно удален из избранного')
