from django.core.validators import MinValueValidator
from django.db import models

from users.models import User

MIN_VALUE = 1

MESSAGE_ERR_TIME = 'Время приготовления должно быть больше ноля.'

MESSAGE_ERR_AMOUNT = 'Количество ингредиентов должно быть больше ноля.'


class Ingredient(models.Model):
    """Модель ингредиентов"""

    name = models.CharField(verbose_name='Ингредиент', max_length=200)
    measurement_unit = models.CharField(
        verbose_name='Единица измерения', max_length=200)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиент'

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Модель тегов"""

    name = models.CharField(verbose_name='Тег', max_length=200)
    color = models.CharField(verbose_name='Цвет HEX-code', max_length=7)
    slug = models.SlugField(verbose_name='Адрес', max_length=200, unique=True)

    class Meta:
        verbose_name = 'Теги'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецептов"""

    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    name = models.CharField(
        verbose_name='Название рецепта',
        max_length=200
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='recipes/images/',
        help_text='Загрузите изображение'
    )
    text = models.TextField(verbose_name='Описание рецепта')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipe')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=[MinValueValidator(MIN_VALUE, message=MESSAGE_ERR_TIME)])
    tags = models.ManyToManyField(Tag, through='TagRecipe')
    pub_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Дата публикации')

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепты'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientRecipe(models.Model):
    """Модель ингредиентов определённого рецепта"""

    recipe = models.ForeignKey(
        Recipe, verbose_name='Рецепт ингредиента',
        related_name='recipe_from_ingredient', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(
        Ingredient, verbose_name='Ингредиент в рецепте',
        related_name='ingredient_for_recipe', on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(
        verbose_name='Количество', blank=False,
        validators=[MinValueValidator(MIN_VALUE, message=MESSAGE_ERR_AMOUNT)])

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['recipe', 'ingredient'],
            name='unique_ingredient',
        )]
        verbose_name = 'Ингредиент для рецепта'
        verbose_name_plural = 'Ингредиент для рецепта'

    def __str__(self):
        return f'{self.recipe} - {self.ingredient}'


class TagRecipe(models.Model):
    """Модель тегов определённого рецепта"""

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['recipe', 'tag'],
            name='unique_tag',
        )]
        verbose_name = 'Теги для рецепта'
        verbose_name_plural = 'Теги для рецепта'

    def __str__(self):
        return f'{self.recipe} - {self.tag}'


class Favorite(models.Model):
    """Модель избранного рецепта"""

    user = models.ForeignKey(
        User, verbose_name='Юзер добавивший в избранное',
        on_delete=models.CASCADE, related_name='is_favorited')
    recipe = models.ForeignKey(
        Recipe, verbose_name='Избранный рецепт', on_delete=models.CASCADE,
        related_name='recipe_in_favorite')

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'recipe'],
            name='unique_favorite',
        )]
        verbose_name = 'Любимый рецепт'
        verbose_name_plural = 'Любимый рецепт'

    def __str__(self):
        return f'{self.recipe} в избранном у {self.user}'


class Subscription(models.Model):
    """Модель подписки"""

    user = models.ForeignKey(
        User, verbose_name='Подписавшийся', on_delete=models.CASCADE,
        related_name='subscriber')
    author = models.ForeignKey(
        User, verbose_name='Подписан на:', on_delete=models.CASCADE,
        related_name='author_recipes')

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'author'],
            name='unique_follow',
        )]
        verbose_name = 'Подписки'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.user} - {self.author}'
