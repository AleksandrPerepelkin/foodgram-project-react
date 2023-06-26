from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.pagination import CustomPagination
from recipes.models import Favorite, Ingredient, Recipe, Subscription, Tag
from shopping_cart.download_cart import download_ingredients
from shopping_cart.models import ShoppingCart
from users.models import User
from .filters import IngredientFilter, RecipeFilter
from .permissions import OwnerOrReadPermission
from .serializers import (IngredientSerializer, RecipeAddSerializer,
                          RecipeSerializer, RecipeSmallSerializer,
                          SubscriptionsSerializer, TagSerializer,
                          FavoriteSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    """Вью сет для рецептов."""

    queryset = Recipe.objects.all()
    permission_classes = (OwnerOrReadPermission,)
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        """Определение сериалайзера для пользователей."""
        if self.action in ('create', 'partial_update'):
            return RecipeAddSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        """Переопределение метода создания поста."""
        serializer.save(author=self.request.user)

    @action(detail=False, methods=('get',),
            url_name='download_shopping_cart',
            permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request, *args, **kwargs):
        """Метод для скачивания списка покупок."""
        ingredients = download_ingredients(request.user)
        return HttpResponse(
            ingredients,
            content_type='text/plain,charset=utf8',
            status=status.HTTP_200_OK,
        )


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Вью сет для тегов."""

    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Вью сет для ингредиентов."""

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class ShoppingCartAPIView(APIView):
    """Вью набор для составления списка покупок."""

    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        """
        Метод добавления существующего рецепта в список покупок пользователя.
        """
        cart = get_object_or_404(Recipe, pk=pk)
        recipe_id = request.data.get('recipe')
        recipe = self.get_recipe(recipe_id)
        quantity = request.data.get('quantity')
        recipe_in_cart = self.add_to_cart(cart, recipe, quantity, request.user)
        serializer = RecipeSmallSerializer(recipe_in_cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, recipe_id):
        """Метод удаления рецепта из списка покупок."""
        recipe_in_cart = ShoppingCart.objects.filter(
            user=request.user, recipe=recipe_id)
        if recipe_in_cart.exists():
            recipe_in_cart.delete()
            return Response({'message':
                             'Recipe successfully removed from shopping list'},
                            status=status.HTTP_204_NO_CONTENT)
        return Response({'message': 'Recipe was not in the shopping list'},
                        status=status.HTTP_400_BAD_REQUEST)

    def get_recipe(self, recipe_id):
        try:
            recipe = Recipe.objects.get(pk=recipe_id)
        except Recipe.DoesNotExist:
            raise Http404
        return recipe

    def add_to_cart(self, cart, recipe, quantity, user):
        recipe_in_cart = ShoppingCart(cart=cart,
                                      recipe=recipe,
                                      quantity=quantity,
                                      user=user)
        recipe_in_cart.save()
        return recipe_in_cart


class FavoriteAPIView(APIView):
    """Вью набора любимых рецептов."""

    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        """
        Метод добавления существующего рецепта,
        в список избранного пользователя.
        """
        recipe = get_object_or_404(Recipe, pk=pk)
        favorite_recipe = Favorite.objects.filter(
            user=request.user, recipe=recipe)
        if favorite_recipe.exists():
            return Response(
                {'error': 'Рецепт уже есть в избранном'},
                status=status.HTTP_400_BAD_REQUEST)
        favorite_recipe = Favorite.objects.create(
            user=request.user, recipe=recipe)
        serializer = FavoriteSerializer(favorite_recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        """Метод удаления рецепта из списка избранных."""
        recipe = get_object_or_404(Recipe, pk=pk)
        favorite_recipe = Favorite.objects.filter(
            user=request.user, recipe=recipe)
        if favorite_recipe.exists():
            favorite_recipe.delete()
            return Response({'message':
                             'Вы уже добавили этот рецепт в избранное'},
                            status=status.HTTP_204_NO_CONTENT)
        return Response({'message': 'Рецепта не было в избранном'},
                        status=status.HTTP_400_BAD_REQUEST)


class SubscribeAPIView(APIView):
    """Вью просмотров для подписок."""

    permission_classes = (IsAuthenticated,)

    def post(self, request, user_id):
        """Метод создания экземпляра подписки."""
        author = get_object_or_404(User, id=user_id)
        if self.request.user == author or Subscription.objects.filter(
                user=request.user, author=user_id).exists():
            return Response(
                {'error': 'Вы пытаетесь подписаться на самого '
                 'себя или уже подписаны на этого автора'},
                status=status.HTTP_400_BAD_REQUEST)
        subscription = Subscription.objects.create(
            author=author, user=self.request.user)
        serializer = SubscriptionsSerializer(
            subscription, context={'request': request})

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, user_id):
        subscription = Subscription.objects.filter(
            user=request.user, author=user_id)
        if subscription.exists():
            subscription.delete()
            return Response({'message': 'Подписка успешно удалена'},
                            status=status.HTTP_204_NO_CONTENT)
        return Response({'message': 'У вас не было такой подписки'},
                        status=status.HTTP_400_BAD_REQUEST)


class SubscriptionsListAPIView(ListAPIView):
    """Вью класс для просмотра списка подписок."""

    serializer_class = SubscriptionsSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPagination

    def get_queryset(self):
        return self.request.user.subscriber.all()
