
from foodLib.DishContainer import DishContainer

class FoodLib(object):
    vegans = 0
    meatEaters = 0

    itemsDatabase = DishContainer()

    veganDishes = []
    meatDishes = []

    def setVegansCount(self, count):
        self.vegans = count

    def setMeatEaters(self, count):
        self.meatEaters = count

    def distributeDishes(self):
            self.veganDishes.clear()
            self.meatDishes.clear()

            dishes = self.itemsDatabase.getDishes(self.vegans, True)

            for dish in dishes:
                self.veganDishes.append(dish)

            dishes = self.itemsDatabase.getDishes(self.meatEaters, False)
            for dish in dishes:
                self.meatDishes.append(dish)

    def showDishes(self, isVegan):

        if isVegan:
            for dish in self.veganDishes:
                print(dish)
        else:
            print("Meat dishes: ")
            for dish in self.meatDishes:
                print(dish)

    def getInfo(self):
        return "Food lib v. 1.0"
