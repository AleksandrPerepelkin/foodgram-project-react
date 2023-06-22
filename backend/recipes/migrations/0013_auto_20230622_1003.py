# Generated by Django 2.2.19 on 2023-06-22 07:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0012_add_unique_to_recipe_ingredient'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favorite',
            options={'verbose_name': 'Любимый рецепт', 'verbose_name_plural': 'Любимый рецепт'},
        ),
        migrations.AlterModelOptions(
            name='ingredient',
            options={'verbose_name': 'Ингредиент', 'verbose_name_plural': 'Ингредиент'},
        ),
        migrations.AlterModelOptions(
            name='ingredientrecipe',
            options={'verbose_name': 'Ингредиент для рецепта', 'verbose_name_plural': 'Ингредиент для рецепта'},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ('-pub_date',), 'verbose_name': 'Рецепты', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.AlterModelOptions(
            name='subscription',
            options={'verbose_name': 'Подписки', 'verbose_name_plural': 'Подписки'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'verbose_name': 'Теги', 'verbose_name_plural': 'Теги'},
        ),
        migrations.AlterModelOptions(
            name='tagrecipe',
            options={'verbose_name': 'Теги для рецепта', 'verbose_name_plural': 'Теги для рецепта'},
        ),
    ]
