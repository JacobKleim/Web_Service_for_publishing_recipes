from django.db.models import Sum

from recipes.models import RecipeIngredient


def generate_shopping_list(user):
    cart_ingredients = (
        RecipeIngredient.objects.filter(
            recipe__cart__user=user
        ).values(
            'ingredients__name',
            'ingredients__measurement_unit',
        ).annotate(cart_amount=Sum('amount')).order_by('-amount')
    )

    shopping_list = ''
    for num, item in enumerate(cart_ingredients):
        name = item['ingredients__name']
        measurement_unit = item['ingredients__measurement_unit']
        amount = item['cart_amount']
        shopping_list += (f'{num + 1}. {name} - '
                          f'{amount} {measurement_unit} \n')

    return shopping_list
