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
