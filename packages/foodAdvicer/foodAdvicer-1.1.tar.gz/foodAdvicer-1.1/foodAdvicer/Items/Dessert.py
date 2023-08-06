


class Dessert(object):
    name = "name not set"
    isVegan = False
    isForChild = False

    def __init__(self, name, isVegan, isForChild):
        self.name = name
        self.isVegan = isVegan
        self.isForChild = isForChild