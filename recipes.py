class Ingredient:
    def __init__(self, name, quantity, unit):
        if quantity <= 0:
            raise ValueError("Количество должно быть больше 0")
        self.name = name
        self.quantity = quantity
        self.unit = unit

    def __str__(self):
        return f"{self.name}: {self.quantity:g} {self.unit}"

    def __eq__(self, other):
        return (
            isinstance(other, Ingredient)
            and self.name == other.name
            and self.unit == other.unit
        )

class Recipe:
    def __init__(self, title, ingredients=None):
        self.title = title
        if ingredients is None:
            self.ingredients = []
        else:
            self.ingredients = ingredients

    def add_ingredient(self, ingredient):
        for item in self.ingredients:
            if item == ingredient:
                item.quantity += ingredient.quantity
                return
        self.ingredients.append(ingredient)

    def scale(self, ratio):
        if ratio <= 0:
            raise ValueError("Коэффициент должен быть больше 0")
        new_ingredients = []
        for ingredient in self.ingredients:
            new_ingredients.append(
                Ingredient(
                    ingredient.name,
                    ingredient.quantity * ratio,
                    ingredient.unit
                )
            )
        return Recipe(self.title, new_ingredients)

    def __len__(self):
        return len(self.ingredients)

    def __str__(self):
        result = self.title + "\n"
        for ingredient in self.ingredients:
            result += str(ingredient) + "\n"
        return result

class DietaryRecipe(Recipe):
    def __init__(self, title, diet_type, ingredients=None):
        super().__init__(title, ingredients)
        self.diet_type = diet_type

    def scale(self, ratio):
        new_recipe = super().scale(ratio)
        return DietaryRecipe(self.title, self.diet_type, new_recipe.ingredients)

    def __str__(self):
        return f"{self.title} ({self.diet_type})"

class ShoppingList:
    def __init__(self):
        self.items = []

    def add_recipe(self, recipe, portions):
        if portions <= 0:
            raise ValueError("Количество порций должно быть больше 0")

        new_recipe = recipe.scale(portions)

        for ingredient in new_recipe.ingredients:
            self.items.append((ingredient, recipe.title))

    def remove_recipe(self, title):
        new_items = []

        for ingredient, recipe_title in self.items:
            if recipe_title != title:
                new_items.append((ingredient, recipe_title))

        self.items = new_items

    def get_list(self):
        result = []

        for ingredient, recipe_title in self.items:
            found = False

            for existing in result:
                if existing == ingredient:
                    existing.quantity += ingredient.quantity
                    found = True
                    break

            if not found:
                result.append(
                    Ingredient(
                        ingredient.name,
                        ingredient.quantity,
                        ingredient.unit
                    )
                )

        result.sort(key=lambda ingredient: ingredient.name)
        return result

    def __add__(self, other):
        new_list = ShoppingList()
        new_list.items = self.items + other.items
        return new_list
    
    