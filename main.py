from typing import Any
import mesa
from mesa.model import Model
import sage
import simpy
import random
import uuid

# fond companies[a1 a2 a3] agents[users] => applicates to buy actions
# delete bonkrote company

############### Functions ################




###### Main classes ######################




class Company(mesa.Agent):
    class Stock:
        def __init__(self, cost):
            self.cost = cost

    def __init__(self, id, capital, Stock, stock_count):
        self.id = id
        self.capital = capital
        self.stock_cost = Stock.cost
        self.stock_count = stock_count

    def getInf(self):
        return (self.capital, self.stock_cost, self.stock_count)

    def step(self) -> None:

        return super().step()


#------------------Users-------------#    

class User(mesa.Agent):
    def __init__(self, unique_id, model) -> None:
        super().__init__(unique_id, model)
        self.sentiment=model.sentiment  #0 - calm; 1 - toxic; 2- ramp (assessment of the current market)
        self.money = 0
        self.ord_list={} #current offers of this User
        self.inv_count=0  
        self.rand_nums=[]
class Fundamentalist(User):
    def __init__(self, unique_id, model, period, goal) -> None:
        super().__init__(unique_id, model)
        self.period=period
        self.max_ord_size=0
        self.goal=goal
        self.booster=1.2 ###where should i take it? 
        self.multiplier=1
    def step(self, model):
        self.base_price=self.goal/self.period*(model.time%self.period)+1
        if(self.base_price>model.min_market_cost):
            self.multiplier=(self.base_price-model.min_market_cost)*self.booster
        else:
            self.multiplier=1
        self.base_size=self.base_price*self.multiplier ####or base_size*...?
        if self.base_size>self.max_ord_size:
            self.max_ord_size=self.base_price 
        for i in self.ord_list.values():
            if i.price<=self.base_price and self.money>=i.t_cost:
                Accept_msg(self.unique_id, i.id_from, i) ###redact!
        for i in model.schedule:
            if i.base_price<=self.base_price: ####total cost <= self.max_ord_size
                a=Order(model, i.base_price) ##to correct



    
################# Models #################
        
#-----------------Messages-----------------------#
class Msg(User):
    def __init__(self, id_from, id_to) -> None:
        self.id_from=id_from
        self.id_to=id_to


class Trade_msg(Msg):
    def __init__(self, model, id_from, id_to, count, cur_price, user_id_from, user_id_to) -> None:
        super().__init__(id_from, id_to)
        self.order=Order(count, cur_price, user_id_from, user_id_to)
        for i in model.schedule:
            if i.unique_id==user_id_from or i.unique_id==user_id_to:
                i.ord_list[self.order.UID]=self.order
                i.inv_count+=1


class Cancel_msg(Msg):
    def __init__(self, id_from, id_to, order, model) -> None:
        super().__init__(id_from, id_to)
        self.UID=order.UUID
        self.id_from=id_from
        self.id_to=id_to
        for i in model.schedule:
            if i.unique_id==self.id_to or i.unique_id==self.id_from:
                i.ord_list[self.UID]

class Accept_msg(Msg):
    def __init__(self, id_from, id_to, order) -> None:
        super().__init__(id_from, id_to)



#-----------------Orders-------------#
class Order():
    def __init__(self, model, price,  count, id_from, id_to, type, time=0) -> None: #QUISTIOPN!# orders to other users or companies? 
        self.id_from=id_from
        self.cur_time=model.time
        self.id_to=id_to
        self.price=price
        self.count=count
        self.UID=uuid.uuid4()
        self.t_cost=price*count
        self.type=type #till canceled or till time: "tc" or "tt"
        if (self.type=="tt"):
            self.time=time
        

    # def __init__(self, count, cur_price, user_id_from, user_id_to) -> None:
    #     self.count=count
    #     self.price=cur_price
    #     self.total_cost=cur_price*count
    #     self.id_from=user_id_from
    #     self.id_to=user_id_to
class m_Order():
    def __init__(self, model, price, count, id_from, company, type) -> None:
        pass

#class process(mesa.Model):



class buying(mesa.Model):
    def __init__(self, N, K):
        self.time=0
        self.min_market_cost=-1
        self.sentiment=0
        self.num__agentsUser = N
        self.num__agentsCompany = K
        self.schedule = mesa.time.RandomActivation()
        # Create agents
        for i in range(self.num_agentsUser):
            a=User(i, self)
            self.schedule.add(a)
        for i in range(self.num__agentsCompany):
            a=Company(self)
            self.schedule.add(a)
    def step(self):
        self.time+=1
        self.min_market_cost=1e9
        for i in self.schedule:
            if i.base_price<self.min_market_cost:
                self.min_market_cost=i.base_price
        self.min_market_cost
        self.schedule.step()
    

############# test #######################

