from api.filters import IngredientFilter, RecipeFilter
from api.permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from api.serializers import (CreateRecipeSerializer, CustomUserSerializer,
                             FavoriteSerializer, FollowSerializer,
                             IngredientSerializer, RecipeSerializer,
                             ShoppingCartSerializer, TagSerializer)
from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import (FavoriteRecipe, Ingredient, RecipeIngredient,
                            Reсipe, ShoppingCart, Tag)
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from users.models import Follow

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 6

    def get_permissions(self):
        if self.action == 'retrieve':
            return [IsAuthenticated(),]
        return super().get_permissions()

    @action(
        methods=['get'],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def subscriptions(self, request, *args, **kwargs):
        queryset = User.objects.filter(following__user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = serializers.SubscriptionSerializer(
            page, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, *args, **kwargs):
        followed_user = get_object_or_404(User, pk=self.kwargs.get('id'))
        serializer = FollowSerializer(
            data={'user': request.user.id, 'following': followed_user.id},
            context={'request': request}
        )
        if request.method == 'POST':
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        try:
            subscription = get_object_or_404(
                Follow, user=request.user, following=followed_user)
        except Http404:
            raise ValidationError({'errors': 'Вы не подписаны'})
        subscription.delete()
        return Response(
            f'Вы отписались от {followed_user}',
            status=status.HTTP_204_NO_CONTENT
        )


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Reсipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = PageNumberPagination
    pagination_class.page_size = 6
    filter_backends = (DjangoFilterBackend, )
    filterset_class = RecipeFilter
    permission_classes = (IsAuthorOrReadOnly | IsAdminOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeSerializer
        return CreateRecipeSerializer

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, *args, **kwargs):
        recipe = get_object_or_404(Reсipe, id=self.kwargs.get('pk'))
        serializer = FavoriteSerializer(
            data={'user': request.user.id, 'recipe': recipe.id},
            context={'request': request}
        )
        if request.method == 'POST':
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        try:
            favorite = get_object_or_404(
                FavoriteRecipe, user=request.user, recipe=recipe)
        except Http404:
            raise ValidationError({'errors': 'Рецепта нет в избранном'})
        favorite.delete()
        return Response(
            'Рецепт удален из избранного',
            status=status.HTTP_204_NO_CONTENT
        )

    @action(
        methods=['post', 'delete'],
        detail=True,
    )
    def shopping_cart(self, request, *args, **kwargs):
        recipe = get_object_or_404(Reсipe, id=self.kwargs.get('pk'))
        serializer = ShoppingCartSerializer(
            data={'user': request.user.id, 'recipe': recipe.id},
            context={'request': request}
        )
        if request.method == 'POST':
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        try:
            favorite = get_object_or_404(
                ShoppingCart, user=request.user, recipe=recipe)
        except Http404:
            raise ValidationError(
                {'errors': 'Рецепта нет в списке покупок'})
        favorite.delete()
        return Response(
            'Рецепт удален из списка покупок',
            status=status.HTTP_204_NO_CONTENT
        )

    @action(
        methods=['get'],
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def download_shopping_cart(self, request):
        cart_ingredients = (
            RecipeIngredient.objects.filter(
                recipe__cart__user=request.user
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

        filename = 'shopping_list.txt'
        response = HttpResponse(shopping_list,
                                content_type='text/plain,charset=utf8')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    permission_classes = (IsAdminOrReadOnly,)
