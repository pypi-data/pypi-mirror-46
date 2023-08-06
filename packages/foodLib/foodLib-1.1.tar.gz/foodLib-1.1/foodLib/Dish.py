
class Dish(object):
    name = "NONE"
    isVegan = False
    
    def __init__(self, name, isVegan):
        self.name = name
        self.isVegan = isVegan

    def __str__(self):
        return "name: " + self.name