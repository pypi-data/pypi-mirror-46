from random import randint
from foodLib.Dish import Dish

class DishContainer(object):
    dishes = []

    def __init__(self):
        self.dishes.append(Dish("veg dish 1", True))
        self.dishes.append(Dish("veg dish 2", True))
        self.dishes.append(Dish("veg dish 3", True))
        self.dishes.append(Dish("veg dish 4", True))
        self.dishes.append(Dish("veg dish 5", True))

        self.dishes.append(Dish("meat dish 1", False))
        self.dishes.append(Dish("meat dish 2", False))
        self.dishes.append(Dish("meat dish 3", False))
        self.dishes.append(Dish("meat dish 4", False))
        self.dishes.append(Dish("meat dish 5", False))

    def getDishes(self, peopleCount, isVegan):
        targetDishes = []
        for i in range(peopleCount):
            while (True):
                randomIndex = randint(0, len(self.dishes) - 1)

                if self.dishes[randomIndex].isVegan != isVegan:
                    continue

                targetDishes.append(self.dishes[randomIndex])
                break

        return targetDishes
