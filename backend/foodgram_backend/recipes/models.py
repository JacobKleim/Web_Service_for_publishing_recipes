from colorfield.fields import ColorField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from recipes.constants import LENGTH, LENGTH_COLOR
from users.models import User


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=LENGTH)
    measurement_unit = models.CharField('Единица измерения', max_length=LENGTH)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        unique_together = ['name', 'measurement_unit']

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField('Название', max_length=LENGTH, unique=True)
    color = ColorField('Цветовой HEX-код', max_length=LENGTH_COLOR)
    slug = models.SlugField('Слаг', max_length=LENGTH, unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Reсipe(models.Model):
    author = models.ForeignKey(
        User, related_name='recipes',
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    name = models.CharField('Название', max_length=LENGTH)
    image = models.ImageField(
        'Изображение',
        upload_to='recipes/images/',
        null=True,
        default=None,
        blank=True
    )
    text = models.TextField('Описание')
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name="recipes",
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(Tag, verbose_name='Теги')
    cooking_time = models.PositiveIntegerField(
        'Время приготовления',
        validators=[
            MinValueValidator(
                1,
                message='Введите число, которое больше или равно 1!'),
            MaxValueValidator(
                1000000,
                message='Введите число, не больше 1000000!')
        ]
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """Модель ингредиента в рецепте"""
    ingredients = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    recipe = models.ForeignKey(
        Reсipe, related_name='recipe_ingredient',
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    amount = models.PositiveIntegerField(
        'Количество',
        validators=[
            MinValueValidator(
                1,
                message='Введите число, которое больше или равно 1!'),
            MaxValueValidator(
                1000000,
                message='Введите число, не больше 1000000!')
        ]
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'

    def __str__(self):
        return f'{self.recipe.name} {self.ingredients.name}'


class AbstractBaseFavorite(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='%(class)s_set',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Reсipe, on_delete=models.CASCADE,
        related_name='%(class)s_set',
        verbose_name='Рецепт'
    )

    class Meta:
        abstract = True


class FavoriteRecipe(AbstractBaseFavorite):
    """Модель избранных рецептов"""

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'

    def __str__(self):
        return f'{self.user} {self.recipe}'


class ShoppingCart(AbstractBaseFavorite):
    """Модель корзины товаров"""

    class Meta:
        verbose_name = 'Корзина покупок'
        verbose_name_plural = 'Корзины покупок'

    def __str__(self):
        return f'{self.user} {self.recipe}'
