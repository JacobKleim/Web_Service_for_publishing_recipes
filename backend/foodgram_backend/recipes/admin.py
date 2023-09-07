from django.contrib import admin
from django.contrib.admin import display

from recipes.models import (FavoriteRecipe, Ingredient, RecipeIngredient,
                            Reсipe, ShoppingCart, Tag)


# class RecipeIngredientInline(admin.TabularInline):
#     model = RecipeIngredient
#     extra = 1
@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('ingredients', 'recipe', 'amount',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug',)


@admin.register(Reсipe)
class RecipeAdmin(admin.ModelAdmin):
    # inlines = (RecipeIngredientInline, )
    list_display = ('name', 'id', 'author', 'added_in_favorites')
    readonly_fields = ('added_in_favorites',)
    list_filter = ('author', 'name', 'tags',)

    @display(description='Количество в избранных')
    def added_in_favorites(self, obj):
        return obj.favorites.count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)


# @admin.register(Follow)
# class FollowAdmin(admin.ModelAdmin):
#     pass
