import mesa
import sage
import simpy

# fond companies[a1 a2 a3] agents[users] => applicates to buy actions
# delete bonkrote company   

class User(mesa.Agent):
    def __init__(self):
        print("I`m User")
class Company(mesa.Agent):
    def __init__(self):
        capital = 0 
        print("I`m Company")

##########################################

class Stock(mesa.Agent):
    def __init__(self):
        print("I`m Stock")

##########################################
class buying(mesa.Model):
    def __init__(self):
        self.user = User()
        self.company = Company()
        self.stock = Stock()

model = buying()