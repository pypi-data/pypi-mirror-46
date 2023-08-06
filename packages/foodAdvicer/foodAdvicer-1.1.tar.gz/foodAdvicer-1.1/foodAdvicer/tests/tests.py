from foodAdvicer.Results.Results import Results
from foodAdvicer.Items.Dessert import Dessert
from foodAdvicer.Items.Dish import Dish
from foodAdvicer.Items.Drink import Drink
from foodAdvicer.ItemsDatabase.ItemsDatabase import ItemsDatabase
from foodAdvicer.FoodAdvicer import FoodAdvicer

if __name__ == '__main__':
    foodAdvicer = FoodAdvicer()
    
    foodAdvicer.setMeetEtaterManNumber(3)
    result = foodAdvicer.resolve()
    print(type(result.dishes))
    print(len(result.dishes))
    for dish in result.dishes:
        print(dish)