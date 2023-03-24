from rest_framework.routers import DefaultRouter

from django.urls import include, path

from api.views import (IngredientViewSet, RecipeViewSet, TagViewSet,
                       CustomUserViewSet)

router = DefaultRouter()
router.register('users', CustomUserViewSet, basename='user')
router.register('tags', TagViewSet, basename='tag')
router.register('ingredients', IngredientViewSet, basename='ingredient')
router.register('recipes', RecipeViewSet, basename='recipe')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
