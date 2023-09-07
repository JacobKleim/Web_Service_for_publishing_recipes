from django.db import models

from users.models import User


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    measurement_unit = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    color = models.CharField(max_length=7)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Reсipe(models.Model):
    author = models.ForeignKey(
        User, related_name='recipes',
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to='recipes/images/',
        null=True,
        default=None,
        blank=True
    )
    text = models.TextField()
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name="recipes"
    )
    tags = models.ManyToManyField(Tag)
    cooking_time = models.PositiveIntegerField()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """Модель ингредиента в рецепте"""
    ingredients = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Reсipe, related_name='recipe_ingredient',
                               on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()


class FavoriteRecipe(models.Model):
    """Модель избранных рецептов"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='favorites')
    recipe = models.ForeignKey(
        Reсipe, on_delete=models.CASCADE,
        related_name='favorites')

    def __str__(self):
        return f'{self.user} {self.recipe}'


class ShoppingCart(models.Model):
    """Модель корзины товаров"""
    user = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='cart')
    recipe = models.ForeignKey(
        Reсipe, on_delete=models.CASCADE,
        related_name='cart')

    def __str__(self):
        return f'{self.user} {self.recipe}'
