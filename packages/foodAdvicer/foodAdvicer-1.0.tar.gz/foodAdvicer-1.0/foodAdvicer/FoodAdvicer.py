

class FoodAdvicer(Object):
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

    def setMeetEtaterManNumber(self, number):
        meetEtaterManNumber = number

    def setMeetEaterWomanNumber(self, number):
        meetEaterWomanNumber = number

    def setMeetEaterChildNumber(self, number):
        meetEaterChildNumber = number

    def setVeganManNumber(self, number):
        veganManNumber = number

    def setVeganWomanNumber(self, number):
        veganWomanNumber = number

    def setVeganChildNumber(self, number):
        veganChildNumber = number

    def setNumberOfMainDishes(self, number):
        numberOfMainDishes = number

    def setNumberOfDesserts(self, number):
        numberOfDesserts = number

    def setBuffet(self, isSet):
        isBuffet = isSet

    def helloWorld(self):
        return "Hello World from library"
