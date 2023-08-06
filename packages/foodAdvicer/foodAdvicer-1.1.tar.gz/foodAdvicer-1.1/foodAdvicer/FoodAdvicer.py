from foodAdvicer.Results.Results import Results
from foodAdvicer.Items.Dessert import Dessert
from foodAdvicer.Items.Dish import Dish
from foodAdvicer.Items.Drink import Drink
from foodAdvicer.ItemsDatabase.ItemsDatabase import ItemsDatabase

class FoodAdvicer(object):
    meetEtaterManNumber = 0
    meetEaterWomanNumber = 0
    meetEaterChildNumber = 0
    veganManNumber = 0
    veganWomanNumber = 0
    veganChildNumber = 0
    numberOfMainDishes = 0
    numberOfDesserts = 0
    #swedish table
    isBuffet = False
    isDessert = False
    isDrinks = False

    itemsDatabase = ItemsDatabase()
    result = Results()

    def setMeetEtaterManNumber(self, number):
        self.meetEtaterManNumber = number

    def setMeetEaterWomanNumber(self, number):
        self.meetEaterWomanNumber = number

    def setMeetEaterChildNumber(self, number):
        self.meetEaterChildNumber = number

    def setVeganManNumber(self, number):
        self.veganManNumber = number

    def setVeganWomanNumber(self, number):
        self.veganWomanNumber = number

    def setVeganChildNumber(self, number):
        self.veganChildNumber = number

    def setNumberOfMainDishes(self, number):
        self.numberOfMainDishes = number

    def setNumberOfDesserts(self, number):
        self.numberOfDesserts = number

    def setBuffet(self, isSet):
        self.isBuffet = isSet

    def resolve(self):
        if not self.isBuffet:
            # print("dishes")
            # print("meetEater")
            choosenDishes = self.itemsDatabase.getDishes(self.meetEtaterManNumber, False, False)
            # print(len(choosenDishes))
            # print(choosenDishes)
            for dish in choosenDishes:
                self.result.dishes.append(dish)

            choosenDishes = self.itemsDatabase.getDishes(self.meetEaterWomanNumber, False, False)
            for dish in choosenDishes:
                self.result.dishes.append(dish)

            choosenDishes = self.itemsDatabase.getDishes(self.meetEaterChildNumber, False, True)
            for dish in choosenDishes:
                self.result.dishes.append(dish)

            # print("Vegan")
            choosenDishes = self.itemsDatabase.getDishes(self.veganManNumber, True, False)
            for dish in choosenDishes:
                self.result.dishes.append(dish)

            choosenDishes = self.itemsDatabase.getDishes(self.veganWomanNumber, True, False)
            for dish in choosenDishes:
                self.result.dishes.append(dish)

            choosenDishes = self.itemsDatabase.getDishes(self.veganChildNumber, True, True)
            for dish in choosenDishes:
                self.result.dishes.append(dish)

            # print("drinks")

            # print("desserts")

            return self.result
        else:
            print("not ready yet")
        return self.result

    def helloWorld(self):
        return "Hello World from library"
