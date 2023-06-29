# Generated by Django 2.2.16 on 2022-12-23 11:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_added_all_models_v1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='ingredient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_for_recipe', to='recipes.Ingredient', verbose_name='Ингредиент в рецепте'),
        ),
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_from_ingredient', to='recipes.Recipe', verbose_name='Рецепт ингредиента'),
        ),
    ]
