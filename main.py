from typing import Any
import mesa
from mesa.model import Model
import sage
import simpy

# fond companies[a1 a2 a3] agents[users] => applicates to buy actions
# delete bonkrote company   

############### Subclasses ################

class Stock(mesa.Agent):
    def __init__(self, cost):
        self.cost=cost
        #print("I`m Stock")

###### Main classes ######################
class User(mesa.Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.money = 0
    #def generate_request(Company, count):
        

class Company(mesa.Agent):
    def __init__(self, capital, Stock, stock_count):
        self.capital = capital
        self.stock_cost = Stock.cost
        self.stock_count = stock_count
    def getInf(self):
        return(self.capital, self.stock_cost, self.stock_count)


######### Models and other functions ########

class buying(mesa.Model, User, Company):
    def __init__(self):
        self.user = User()
        self.company = Company()
        self.stock = Stock()

############# test #######################

a=Stock(13)
b=Company(650, a, 13)
print(*b.getInf())

