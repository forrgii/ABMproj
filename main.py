from typing import Any
import mesa
from mesa.model import Model
import sage
import simpy

# fond companies[a1 a2 a3] agents[users] => applicates to buy actions
# delete bonkrote company   

############### Functions ################

#pair structure 
def make_pair(x,y):
    return lambda n: x if n==0 else y
def first(p):
    return p(0)

def second(p):
    return p(1)

###### Main classes ######################      

class Company(mesa.Agent):
    class Stock():
        def __init__(self, cost):
            self.cost = cost

    def __init__(self, name, id, capital, Stock, stock_count):
        
        self.name = name
        self.id = id
        self.capital = capital
        self.stock_cost = Stock.cost
        self.stock_count = stock_count

    def getInf(self):
        return(self.capital, self.stock_cost, self.stock_count)

class User(mesa.Agent):
    def __init__(self, unique_id, model) -> None:
        super().__init__(unique_id, model)
        self.money = 0
        self.history = [] #name of company, one stock cost, count of stocks
        self.account = []
    def getHist(self):
        return(self.history)
    
    #buying of stocks
    def ReqBuy(self, count, Company):
        if(self.money>Company.stock_cost * count and Company.stock_count <= count):
            self.money -= Company.stock_cost * count
            Company.stock_count -= count
            Company.capital += Company.stock_cost * count
            #name of company, one stock cost, count of stocks
            self.offer=(Company.id, Company.stock_cost, count, "Bought")
            self.history.push_back(self.offer)
            #acc def
            index=0
            for i in self.account:
                if(first(i)==Company.id):
                    index=self.account.index(i)
                    break
            if (index):
                self.account[index][1]+=count
            else:
                offer=make_pair(Company.id, count)
                self.account.push_back(offer)
        else:
            print("wrong request")

    #selling of stocks
    def ReqSell(self, count, Company):
        for i in self.account: 
                if (first(i) == Company.id):
                    if(Company.capital > Company.stock_cost * count and second(i)>=count):
                        self.money += Company.stock_cost * count
                        Company.stock_count += count
                        Company.capital -= Company.stock_cost * count
                        #name of company, one stock cost, count of stocks
                        self.offer = (Company.id, Company.stock_cost, count, "Selled")
                        self.history.push_back(self.offer)
                        #acc def
                        i[1] -= count
                        if(second(i)==0):
                            self.account.remove(i)
                    else:
                        print("wrong request")
                    break

        

################# Models #################

class buying(mesa.Model, User, Company):
    def __init__(self):
        self.user = User()
        self.company = Company()

############# test #######################

a=Company.Stock(13)
b=Company(650, a, 13)
print(*b.getInf())

