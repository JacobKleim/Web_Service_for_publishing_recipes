from django_filters.rest_framework import FilterSet, filters

from recipes.models import Ingredient, Reсipe, Tag


class IngredientFilter(FilterSet):
    name = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)


class RecipeFilter(FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
    )
    is_favorited = filters.BooleanFilter(method='get_favorited')
    is_in_shopping_cart = filters.BooleanFilter(method='get_in_shopping_cart')

    class Meta:
        model = Reсipe
        fields = ('author', 'tags',)

    def get_favorited(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return Reсipe.objects.filter(
                favoriterecipe_set__user=self.request.user)
        return Reсipe.objects.filter(
            favoriterecipe_set__user=self.request.user)

    def get_in_shopping_cart(self, queryset, name, value):
        if value and self.request.user.is_authenticated:
            return queryset.filter(shoppingcart_set__user=self.request.user)
        return queryset
