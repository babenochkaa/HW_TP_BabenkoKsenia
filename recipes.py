class Ingredient:
    def __init__(self, name, quantity, unit):
        if quantity <= 0:
            raise ValueError("Количество должно быть больше 0")
        self.name = name
        self.quantity = quantity
        self.unit = unit

    def __str__(self):
        return f"{self.name}: {self.quantity} {self.unit}"

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