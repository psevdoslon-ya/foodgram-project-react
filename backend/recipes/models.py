from django.db import models
from django.contrib.auth import get_user_model
from django.core import validators


User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Наменование тега',
        max_length=200,
        unique=True
    )
    color = models.CharField(
        verbose_name='HEX-код цвета',
        max_length=7,
        unique=True,
        db_index=False
    )
    slug = models.SlugField(
        verbose_name='Slug тега',
        max_length=200,
        unique=True,
        db_index=False,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        verbose_name='Название ингридиента',
        max_length=200
    )
    measurement_unit = models.CharField(
        verbose_name='Единица измерения',
        max_length=50
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор рецепта',
        related_name='recipes',
        on_delete=models.CASCADE
    )
    name = models.CharField(
        verbose_name='Наменование тега',
        max_length=200
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='recipe_images/'
    )
    text = models.TextField(
        verbose_name='Описание блюда',
        help_text='Введите описание вашего рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингридиенты',
        related_name='recipes',
        through='IngredientInRecipe'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги',
        related_name='recipes'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=(validators.MinValueValidator(
            1, message='Минимальное время приготовления блюда - 1 минута!'),
        )
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True,
        editable=False
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientInRecipe(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        related_name='ingredientinrecipe',
        on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Ингридиент',
        related_name='ingredientinrecipe',
        on_delete=models.CASCADE
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество',
        validators=(validators.MinValueValidator(
            1, message='Минимальное количество ингридиентов - 1!'),
        )
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Количество ингридиентов'

    def __str__(self):
        return f'{self.ingredient} -> {self.amount}'


class ShoppingList(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Ингридиенты из рецептов',
        related_name='ShoppingLists',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        verbose_name='Обладатель списка',
        related_name='ShoppingLists',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return f'{self.recipe} -> {self.user}'


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Любимый рецепт',
        related_name='favorites',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='favorites',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Любимый рецепт'
        verbose_name_plural = 'Любимые рецепты'

    def __str__(self):
        return f'{self.recipe} -> {self.user}'
