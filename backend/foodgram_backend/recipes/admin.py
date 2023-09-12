from django import forms
from django.contrib import admin
from django.contrib.admin import display

from recipes.models import (FavoriteRecipe, Ingredient, RecipeIngredient,
                            Reсipe, ShoppingCart, Tag)


class RecipeAdminForm(forms.ModelForm):
    class Meta:
        model = Reсipe
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        ingredients = cleaned_data.get('ingredients')
        tags = cleaned_data.get('tags')

        if not ingredients:
            raise forms.ValidationError('Добавьте хотя бы один ингредиент.')

        if not tags:
            raise forms.ValidationError('Добавьте хотя бы один тег.')


class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount')

        if amount <= 0:
            raise forms.ValidationError(
                'Количество ингредиента должно быть больше 0.')


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1


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
    list_display = ('name', 'id', 'author', 'added_in_favorites')
    inlines = (RecipeIngredientInline, )
    readonly_fields = ('added_in_favorites',)
    list_filter = ('author', 'name', 'tags',)

    @display(description='Количество в избранных')
    def added_in_favorites(self, obj):
        return obj.favoriterecipe_set.count()

    def get_ingredients_display(self, obj):
        return ", ".join(
            [str(ingredient) for ingredient in obj.ingredients.all()])


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)
