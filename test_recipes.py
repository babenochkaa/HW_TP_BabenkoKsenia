import pytest
from recipes import Ingredient, Recipe, ShoppingList, DietaryRecipe


def test_ingredient_creation():
    ingredient = Ingredient("Мука", 500, "г")

    assert ingredient.name == "Мука"
    assert ingredient.quantity == 500.0
    assert ingredient.unit == "г"


def test_ingredient_str():
    ingredient = Ingredient("Мука", 500, "г")

    assert str(ingredient) == "Мука: 500.0 г"


def test_ingredient_eq():
    ingredient1 = Ingredient("Мука", 500, "г")
    ingredient2 = Ingredient("Мука", 300, "г")
    ingredient3 = Ingredient("Сахар", 500, "г")
    ingredient4 = Ingredient("Мука", 500, "кг")

    assert ingredient1 == ingredient2
    assert ingredient1 != ingredient3
    assert ingredient1 != ingredient4


def test_ingredient_negative_quantity():
    with pytest.raises(ValueError):
        Ingredient("Мука", -100, "г")


def test_recipe_creation():
    ingredient = Ingredient("Мука", 500, "г")
    recipe = Recipe("Пирог", [ingredient])

    assert recipe.title == "Пирог"
    assert recipe.ingredients == [ingredient]


def test_add_ingredient_new():
    recipe = Recipe("Пирог")
    ingredient = Ingredient("Мука", 500, "г")

    recipe.add_ingredient(ingredient)

    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0].quantity == 500.0


def test_add_ingredient_existing():
    recipe = Recipe("Пирог")
    recipe.add_ingredient(Ingredient("Мука", 500, "г"))
    recipe.add_ingredient(Ingredient("Мука", 200, "г"))

    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0].quantity == 700.0


def test_recipe_scale():
    recipe = Recipe("Пирог", [
        Ingredient("Мука", 500, "г"),
        Ingredient("Сахар", 100, "г")
    ])

    scaled_recipe = recipe.scale(2)

    assert scaled_recipe is not recipe
    assert scaled_recipe.ingredients[0].quantity == 1000.0
    assert scaled_recipe.ingredients[1].quantity == 200.0

    assert recipe.ingredients[0].quantity == 500.0
    assert recipe.ingredients[1].quantity == 100.0


def test_recipe_scale_invalid_ratio():
    recipe = Recipe("Пирог", [Ingredient("Мука", 500, "г")])

    with pytest.raises(ValueError):
        recipe.scale(0)


def test_recipe_len():
    recipe = Recipe("Пирог")
    recipe.add_ingredient(Ingredient("Мука", 500, "г"))
    recipe.add_ingredient(Ingredient("Сахар", 100, "г"))

    assert len(recipe) == 2


def test_dietary_recipe_scale():
    recipe = DietaryRecipe("Пирог", "веган", [
        Ingredient("Мука", 500, "г")
    ])

    scaled_recipe = recipe.scale(2)

    assert isinstance(scaled_recipe, DietaryRecipe)
    assert scaled_recipe.diet_type == "веган"
    assert scaled_recipe.ingredients[0].quantity == 1000.0


def test_shopping_list_add_recipe():
    recipe = Recipe("Пирог", [
        Ingredient("Мука", 500, "г")
    ])

    shopping_list = ShoppingList()
    shopping_list.add_recipe(recipe, 2)

    result = shopping_list.get_list()

    assert len(result) == 1
    assert result[0].name == "Мука"
    assert result[0].quantity == 1000.0


def test_shopping_list_add_recipe_invalid_portions():
    recipe = Recipe("Пирог", [
        Ingredient("Мука", 500, "г")
    ])

    shopping_list = ShoppingList()

    with pytest.raises(ValueError):
        shopping_list.add_recipe(recipe, 0)


def test_shopping_list_remove_recipe():
    recipe1 = Recipe("Пирог", [
        Ingredient("Мука", 500, "г")
    ])

    recipe2 = Recipe("Блины", [
        Ingredient("Молоко", 300, "мл")
    ])

    shopping_list = ShoppingList()
    shopping_list.add_recipe(recipe1, 1)
    shopping_list.add_recipe(recipe2, 1)

    shopping_list.remove_recipe("Пирог")

    result = shopping_list.get_list()

    assert len(result) == 1
    assert result[0].name == "Молоко"


def test_shopping_list_remove_unknown_recipe():
    recipe = Recipe("Пирог", [
        Ingredient("Мука", 500, "г")
    ])

    shopping_list = ShoppingList()
    shopping_list.add_recipe(recipe, 1)

    shopping_list.remove_recipe("Неизвестный рецепт")

    result = shopping_list.get_list()

    assert len(result) == 1


def test_shopping_list_get_list_sums_and_sorts():
    recipe1 = Recipe("Пирог", [
        Ingredient("Мука", 500, "г"),
        Ingredient("Сахар", 100, "г")
    ])

    recipe2 = Recipe("Блины", [
        Ingredient("Мука", 300, "г"),
        Ingredient("Молоко", 200, "мл")
    ])

    shopping_list = ShoppingList()
    shopping_list.add_recipe(recipe1, 1)
    shopping_list.add_recipe(recipe2, 1)

    result = shopping_list.get_list()

    assert [ingredient.name for ingredient in result] == ["Молоко", "Мука", "Сахар"]

    flour = [ingredient for ingredient in result if ingredient.name == "Мука"][0]
    assert flour.quantity == 800.0


def test_shopping_list_add():
    recipe1 = Recipe("Пирог", [
        Ingredient("Мука", 500, "г")
    ])

    recipe2 = Recipe("Блины", [
        Ingredient("Молоко", 300, "мл")
    ])

    list1 = ShoppingList()
    list2 = ShoppingList()
    list1.add_recipe(recipe1, 1)
    list2.add_recipe(recipe2, 1)
    list3 = list1 + list2
    assert len(list3.get_list()) == 2
    assert len(list1.get_list()) == 1
    assert len(list2.get_list()) == 1