from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Favorite, Ingredient, IngredientInRecipe, Recipe,
                            ShoppingList, Tag)
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.validators import ValidationError
from rest_framework.viewsets import ReadOnlyModelViewSet

from .filters import TagFilter
from .pagination import CustomPageNumberPagination
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import (GetRecipeSerializer, IngredientSerializer,
                          RecipeSerializer, ShortRecipeSerializer,
                          TagSerializer)

User = get_user_model()


class TagViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                 viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        name = self.request.query_params.get('name')
        return self.queryset.filter(name__istartswith=name)


class RecipeViewSet(viewsets.ModelViewSet):
    # queryset = Recipe.objects.all()
    pagination_class = CustomPageNumberPagination
    permission_classes = (IsOwnerOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filter_class = TagFilter

    def get_queryset(self):
        tags = self.request.query_params.getlist('tags')
        if tags:
            return Recipe.objects.filter(tags__slug__in=tags).distinct()
        return Recipe.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return GetRecipeSerializer
        return RecipeSerializer

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(author=user)

    def create_recipe(self, model, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = self.request.user
        if model.objects.filter(recipe=recipe, user=user).exists():
            raise ValidationError('Рецепт уже добавлен!')
        model.objects.create(recipe=recipe, user=user)
        serializer = ShortRecipeSerializer(recipe)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def delete_recipe(self, model, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = self.request.user
        obj = get_object_or_404(model, recipe=recipe, user=user)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, permission_classes=[IsAuthenticated],
            methods=['POST', 'DELETE'])
    def favorite(self, request, pk):
        if self.request.method == 'POST':
            return self.create_recipe(Favorite, request, pk)
        return self.delete_recipe(Favorite, request, pk)

    @action(detail=True, permission_classes=[IsAuthenticated],
            methods=['POST', 'DELETE'])
    def shopping_cart(self, request, pk):
        if self.request.method == 'POST':
            return self.create_recipe(ShoppingList, request, pk)
        return self.delete_recipe(ShoppingList, request, pk)

    @action(detail=False, methods=['GET'],
            permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        user = self.request.user
        if not user.shoppinglists.exists():
            return Response(status.HTTP_400_BAD_REQUEST)

        file_name = f'{user.username}_shopping_list.txt'
        shopping_list = ['Список покупок:\n']
        ingredients = IngredientInRecipe.objects.filter(
            recipe__shoppinglists__user=request.user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).order_by(
            'ingredient__name'
        ).annotate(ingredient_sum=Sum('amount'))

        for ingredient in ingredients:
            name = ingredient['ingredient__name']
            measurement_unit = ingredient['ingredient__measurement_unit']
            amount = ingredient['ingredient_sum']
            shopping_list.append(f'{name} -> {amount} ({measurement_unit})')
        shopping_list.append('\nCalculated in Foodgram by Timon.')
        content = '\n'.join(shopping_list)
        response = HttpResponse(content,
                                content_type='text.txt; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename={file_name}'
        return response
