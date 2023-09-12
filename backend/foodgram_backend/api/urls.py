from django.urls import include, path
from rest_framework import routers

from api.views import (CustomUserViewSet, IngredientViewSet, RecipeViewSet,
                       TagViewSet)


router = routers.DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')
router.register('tags', TagViewSet, basename='tags')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('ingredients', IngredientViewSet, basename='ingredients')


urlpatterns = [
    path('api/', include(router.urls)),
    path('api/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls))
]
