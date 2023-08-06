

class Dish(object):
    name = "name not set"
    isVegan = False
    isForChild = False
    
    def __init__(self, name, isVegan, isForChild):
        self.name = name
        self.isVegan = isVegan
        self.isForChild = isForChild

    def __str__(self):
        return "name: %s, isVegan: %d, isForChild: %d" % (self.name, self.isVegan, self.isForChild)