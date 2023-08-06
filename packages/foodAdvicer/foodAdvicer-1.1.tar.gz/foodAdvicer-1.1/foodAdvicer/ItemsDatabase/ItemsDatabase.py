from random import randint

from foodAdvicer.Items.Dessert import Dessert
from foodAdvicer.Items.Dish import Dish
from foodAdvicer.Items.Drink import Drink

class ItemsDatabase(object):
    dishes = []
    desserts = []
    drinkables = []

    def __init__(self):
        self.dishes.append(Dish("sałatka jarzynowa", True, True))
        self.dishes.append(Dish("rosół", False, True))
        self.dishes.append(Dish("naleśniki", False, True))
        self.dishes.append(Dish("danie 1", True, True))
        self.dishes.append(Dish("danie 2", False, False))
        self.dishes.append(Dish("danie 3 ", True, False))
        self.dishes.append(Dish("danie 4", True, False))
        # for dish in self.dishes:
        #     print(dish)

    def getDishes(self, number, isVegan, isForChild):
        results = []
        for i in range(number):
            dish = "notSet"
            while (True):
                # print("i:%d, number: %d" % (i, number))
                randomIndex = randint(0, len(self.dishes) - 1)
                # print(self.dishes[randomIndex])
                # print(randomIndex)
                if self.dishes[randomIndex].isVegan != isVegan:
                    # print("invalid dish: %s" % self.dishes[randomIndex])
                    continue
                elif self.dishes[randomIndex].isForChild != isForChild:
                    # print("invalid 2 dish: %s" % self.dishes[randomIndex])
                    continue
                # valid dish, append, brake
                # print("valid dish: %s" % self.dishes[randomIndex])
                results.append(self.dishes[randomIndex])
                break
        # print("from database")
        # for dish in results:
            # print(dish)

        # print(results)
        return results
