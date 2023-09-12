from django.db.models import F
from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField

from recipes.models import (FavoriteRecipe, Ingredient, RecipeIngredient,
                            Reсipe, ShoppingCart, Tag)
from users.models import Follow, User


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'password'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        return Follow.objects.filter(
            user=request.user, following=obj.id).exists()

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class PreviewRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reсipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscriptionSerializer(CustomUserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = obj.recipes.all()
        if limit:
            recipes = recipes[:int(limit)]
        serializer = PreviewRecipeSerializer(recipes,
                                             many=True,
                                             read_only=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return Reсipe.objects.filter(author=obj.id).count()


class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = ('user', 'following')
        validators = (
            serializers.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
                message=('Подписка уже оформлена')
            ),
        )

    def validate(self, data):
        if data.get('user') == data.get('following'):
            raise serializers.ValidationError(
                {'errors': 'Нельзя подписаться на себя'})
        return data

    def create(self, validated_data):
        return Follow.objects.create(**validated_data)

    def to_representation(self, instance):
        return SubscriptionSerializer(
            instance=instance.following,
            context={'request': self.context.get('request')}
        ).data


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def validate_amount(self, value):
        amount = value
        if amount <= 0:
            raise ValidationError(
                {'measurement_unit':
                 'Количество ингредиентов должно быть больше 0!'})
        return value


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Reсipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_ingredients(self, obj):
        recipe = obj
        ingredients = recipe.ingredients.values(
            'id',
            'name',
            'measurement_unit',
            amount=F('recipeingredient__amount')
        )
        return ingredients

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return FavoriteRecipe.objects.filter(
            recipe=obj, user=request.user).exists()

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(
            recipe=obj, user=request.user).exists()


class CreateRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True)
    ingredients = RecipeIngredientSerializer(many=True)
    cooking_time = serializers.IntegerField()
    name = serializers.CharField()

    class Meta:
        model = Reсipe
        fields = (
            'tags',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def validate_name(self, value):
        name = value
        if not any(char.isalpha() for char in name):
            raise serializers.ValidationError(
                {'name':
                 'Название не может содержать только цифры и знаки.'})
        return value

    def validate_ingredients(self, value):
        ingredients = value
        ingredients_list = []
        for item in ingredients:
            ingredient = item['id']
            if ingredient in ingredients_list:
                raise ValidationError({
                    'ingredients': 'Ингридиенты не могут повторяться!'
                })
            ingredients_list.append(ingredient)
        return value

    def validate_tags(self, value):
        tags = value
        if not tags:
            raise ValidationError(
                {'tags': 'Нужно выбрать хотя бы один тег!'})
        tags_list = []
        for tag in tags:
            if tag in tags_list:
                raise ValidationError(
                    {'tags': 'Теги должны быть уникальными!'})
            tags_list.append(tag)
        return value

    def validate_cooking_time(self, value):
        cooking_time = value
        if cooking_time <= 0:
            raise ValidationError(
                {'cooking_time': 'Время должно быть больше 0!'})
        return value

    def add_tags_ingredients(self, ingredients, tags, model):
        recipeingredients_data = []
        for ingredient in ingredients:
            recipeingredients_data.append(RecipeIngredient(
                recipe=model,
                ingredients=ingredient['id'],
                amount=ingredient['amount']
            ))
        RecipeIngredient.objects.bulk_create(recipeingredients_data)

        recipetags_data = []
        for tag in tags:
            recipetags_data.append(Tag.objects.get(id=tag.id))
        model.tags.add(*recipetags_data)

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = super().create(validated_data)
        self.add_tags_ingredients(ingredients, tags, recipe)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.ingredients.clear()
        instance.tags.clear()
        self.add_tags_ingredients(ingredients, tags, instance)
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return RecipeSerializer(
            instance=instance,
            context={'request': self.context.get('request')}
        ).data


class AbstractFavoriteShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True

    def to_representation(self, instance):
        return PreviewRecipeSerializer(
            instance=instance.recipe,
            context={'request': self.context.get('request')}
        ).data


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteRecipe
        fields = ('user', 'recipe')


class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe')
