
import heapq
import random
from numpy.random import choice
import math
#from lcgrand import *
#import matplotlib.pyplot as plt
IDLE = 0
BUSY = 1
hot_food=0
Specialty_sandwich=1
drinks=2
cashier=3


def exponential(mean):
    return random.expovariate(1/mean)
    #return -(1 / rate) * math.log(lcgrand(1))

def uniform_random(lo,hi): 
    return random.uniform(lo, hi)


# Parameters
class Params:
    def __init__(self, group_size,group_prob,arrival_t,run_time,routing, route_prob,employee_count,st_u,act_u):
        self.lambd = arrival_t  # interarrival rate
        self.group_size=group_size
        self.group_prob=group_prob
        self.run_time=run_time
        self.routing=routing
        self.st_u=st_u
        self.act_u=act_u
        self.route_prob=route_prob
        self.employee_count=employee_count
        self.group_id=0
        self.mydict=dict()
        #print( self.route_prob)

    # Note lambd and mu are not mean value, they are rates i.e. (1/mean)


# Write more functions if required


# States and statistical counters
class States:
    def __init__(self):
        # States
        self.queue = []
        # Declare other states variables that might be needed
        self.time_last_event = 0.0

        # Statistics
        self.server_busy_count=[]
        self.cashier_busy_count=[]
        self.counter_delay=[0,0,0,0]
        self.customer_delay=[0,0,0]
        self.served_counter=[0,0,0,0]
        self.total_num_custs=0
        self.current_customers=0
        self.avg_customer_in_system=0
        self.max_customers=-math.inf
        self.max_food_q_len=[-math.inf,-math.inf]
        self.max_cashier_q_len=[]
        self.avg_food_q_len=[0,0]
        self.avg_cashier_q_len=0
        self.avg_q_delay_counter=[0,0,0,0]
        self.avg_q_delay_customer=[0,0,0]
        self.total_arrival_cust_type=[0,0,0]
        self.total_served=0

    def update(self, sim, event):
        time_since_last_event = event.eventTime - self.time_last_event
        self.avg_customer_in_system+= time_since_last_event * self.current_customers
        if self.current_customers > self.max_customers:
            self.max_customers=self.current_customers
        if len(self.queue[0]) > self.max_food_q_len[0]:
            self.max_food_q_len[0]=len(self.queue[0])

        if len(self.queue[1]) > self.max_food_q_len[1]:
            self.max_food_q_len[1]=len(self.queue[1])

        for i in range(sim.params.employee_count[3]):
            if len(self.queue[3][i])> self.max_cashier_q_len[i] :
                self.max_cashier_q_len[i]=len(self.queue[3][i])    

        self.avg_food_q_len[0]+= time_since_last_event*len(self.queue[0])
        self.avg_food_q_len[1]+= time_since_last_event*len(self.queue[1]) 

        for i in range(sim.params.employee_count[3]):
            self.avg_cashier_q_len+= time_since_last_event* len(self.queue[3][i])    




        self.time_last_event = event.eventTime

    def finish(self, sim):
        self.avg_customer_in_system=self.avg_customer_in_system/(sim.simclock)
        self.avg_food_q_len[0]=self.avg_food_q_len[0]/(sim.simclock)
        self.avg_food_q_len[1]=self.avg_food_q_len[0]/(sim.simclock)
        self.avg_cashier_q_len=self.avg_cashier_q_len/(sim.simclock*sim.params.employee_count[3])
        try:
            for i in range(4):
                if i!=2:
                    self.avg_q_delay_counter[i]=self.counter_delay[i]/self.served_counter[i]
        except ZeroDivisionError:
                print("zero division error .served 0")            
        
        try:
            for i in range(3):
                self.avg_q_delay_customer[i]=self.customer_delay[i]/self.total_arrival_cust_type[i]
        except ZeroDivisionError:
                print("zero division error .arrive 0")       



        print('\n\naverage num of customers',self.avg_customer_in_system)
        print('Maximum customers in the system',self.max_customers)

        print('\n\nFood counter No\t\tMaximum queue length')
        print(0,'\t\t\t\t',self.max_food_q_len[0],'\n',1,'\t\t\t\t',self.max_food_q_len[1])

        print('\n\ncashier counter queue No\tMaximum queue length')
        for i in range(sim.params.employee_count[3]):
            print(i,'\t\t\t\t',self.max_cashier_q_len[i])

        print('\n\nFood counter No\t\tAverage queue length')
        print(0,'\t\t\t\t',self.avg_food_q_len[0],'\n',1,'\t\t\t\t',self.avg_food_q_len[1])  

        print('\n\ncashier counter avg_q_length\t:',self.avg_cashier_q_len)  

        print('\nCounter No.\t\t\t\tAverage Q delay')
        for i in range(4):
            if i!=2:
                print(i,'\t\t\t\t',self.avg_q_delay_counter[i])
        
        print('\nCustomer Type\t\t\t\tAverage Q delay')
        for i in range(3):
            print(i,'\t\t\t\t',self.avg_q_delay_customer[i])

        print('total customers arrived ',self.total_num_custs)
        print('total customers served ',self.total_served)
        print('final global group_id',sim.params.group_id)


        pass

    def printResults(self, sim):
        pass
    def getResults(self, sim):
        pass


# Write more functions if required


class Event:
    def __init__(self, sim):
        self.eventType = None
        self.sim = sim
        self.eventTime = None
        self.groupNum=None
        self.customerType=None
        self.currentCounter=None #index, specifies where the job is in its routing.
        self.queueNum=None 
        self.route=None
        self.gid=None
    def process(self, sim):
        raise Exception('Unimplemented process method for the event!')

    def __repr__(self):
        return self.eventType

    def __lt__(self,other):
        return True
    def __gt__(self,other):
        return True    
    def __le__(self,other):
        return True
    def __ge__(self,other):
        return True
    def __eq__(self,other):
        return True
    def __ne__(self,other):
        return True        

class StartEvent(Event):
    def __init__(self, eventTime, sim):
        super().__init__(sim)
        self.eventTime = eventTime
        self.eventType = 'START'
        self.sim = sim
        self.groupNum=None
        self.customerType=None
        self.currentCounter=None
        self.queueNum=None
        self.route=None
        self.gid=None

    def process(self, sim):
        group=choice(sim.params.group_size,p=sim.params.group_prob)
        print('group choice',group)
        sim.params.mydict[sim.params.group_id]="unused"
        print('group_id',sim.params.group_id)
        for i in range(group):
            atime = self.eventTime + exponential(self.sim.params.lambd)
            currentCounter=0
            queueNum=0
            customerType=choice([0,1,2],p=sim.params.route_prob)
            route=sim.params.routing[customerType]
            #print('route  in start------------------------------------',route)

            sim.scheduleEvent(ArrivalEvent(atime,sim,group,currentCounter,queueNum,route,customerType,sim.params.group_id))
       
        sim.scheduleEvent(ExitEvent(5400, self.sim))


class ExitEvent(Event):
    def __init__(self, eventTime, sim):
        super().__init__(sim)
        self.eventTime = eventTime
        self.eventType = 'EXIT'
        self.sim = sim

    def process(self, sim):
        print("simulation ends at :", self.eventTime)


class ArrivalEvent(Event):
    # Write __init__ function
    def __init__(self, eventTime, sim,group,currentCounter,queueNum,route,customerType,gid):
        super().__init__(sim)
        self.eventTime = eventTime
        self.eventType = 'ARRIVAL'
        self.sim = sim
        self.groupNum=group
        self.customerType=customerType
        self.currentCounter=currentCounter
        self.queueNum=queueNum
        self.route=route
        self.gid=gid

    def process(self, sim):
        # Complete this function
        sim.states.total_num_custs+=1
        sim.states.total_arrival_cust_type[self.customerType]+=1
        #print('currentCounter',self.currentCounter)
        #print('arrival bahir  route----------------',self.route)

        counter = self.route[self.currentCounter]

        if self.currentCounter==0:
            sim.states.total_num_custs+=1
            sim.states.current_customers+=1
            if (self.gid in sim.params.mydict) and sim.params.mydict[self.gid] =="unused":
                print('unused group_id')
                sim.params.mydict[self.gid]="used"
                sim.params.group_id+=1
                sim.params.mydict[sim.params.group_id]="unused"
                group=choice(sim.params.group_size,p=sim.params.group_prob)
                print('group choice',group)
                print('group_id',sim.params.group_id)
                for i in range(group):
                    atime = self.eventTime + exponential(self.sim.params.lambd)
                    currentCounter=0
                    queueNum=0
                    customerType=choice([0,1,2],p=sim.params.route_prob)
                    route=sim.params.routing[customerType]
                    #print('route in arrival currcounter------------------',route)

                    sim.scheduleEvent(ArrivalEvent(atime,sim,group,currentCounter,queueNum,route,customerType,sim.params.group_id))

        #busy &  applicable for food
        if (counter ==0 or counter ==1) and sim.states.server_busy_count[counter] > 0 : 
            print('busy food queue')
            sim.states.queue[counter].append(self)  ##for hot food & sandwich
        #for  busy cashier    
        elif counter ==3 and sim.states.server_busy_count[3] == sim.params.employee_count[3]: 
            print('busy cashier queue')
            min_len=math.inf
            min_q=0 
            for i in range(sim.params.employee_count[3]):
                if len(sim.states.queue[3][i]) < min_len:
                    min_q=i
                    min_len=len(sim.states.queue[3][i])
            self.queueNum=min_q        
            sim.states.queue[3][min_q].append(self)  

        # not busy         
        else: 
            sim.states.server_busy_count[counter]+=1
            sim.states.served_counter[counter]+=1
            if counter !=3: # for foood and drinks
                print('taking service from counter',counter)
                dtime = self.eventTime + uniform_random(sim.params.st_u[counter][0],sim.params.st_u[counter][1])
                sim.scheduleEvent(DepartureEvent(dtime, sim,self.groupNum,self.customerType,self.currentCounter,self.queueNum,self.route,self.gid))

            #for cashier    
            else:
                print('taking service from  counter',counter)
                if self.customerType == 2: #for only drinks customer type
                    dtime = self.eventTime + uniform_random(sim.params.act_u[2][0],sim.params.st_u[2][1])
                else: 
                    dtime = self.eventTime + uniform_random(sim.params.act_u[2][0],sim.params.st_u[2][1])+uniform_random(sim.params.act_u[self.customerType][0],sim.params.st_u[self.customerType][1])

                for i in range(sim.params.employee_count[3]):
                    if sim.states.cashier_busy_count[i] ==0:
                        sim.states.cashier_busy_count[i]=1
                        self.queueNum=i
                        break
                sim.scheduleEvent(DepartureEvent(dtime, sim,self.groupNum,self.customerType,self.currentCounter,self.queueNum,self.route,self.gid))        


class DepartureEvent(Event):
    # Write __init__ function
    def __init__(self, eventTime, sim,groupNum,customerType,currentCounter,queueNum,route,gid):
        super().__init__(sim)
        self.eventTime = eventTime
        self.eventType = 'DEPART'
        self.sim = sim
        self.groupNum=groupNum
        self.customerType=customerType
        self.currentCounter=currentCounter
        self.queueNum=queueNum
        self.route=route
        self.gid=gid

    def process(self, sim):
        counter=self.route[self.currentCounter]

        #shedule arrival for next counter 
        if self.currentCounter ==(len(self.route)-1):
            print('departure last counter in its routing' )
            sim.states.current_customers-=1
            sim.states.total_served+=1
        else:
            print('departure counter in its routing of counter',self.currentCounter )
            currentCounter=self.currentCounter+1
            atime=self.eventTime
            #eventTime, sim,group,currentCounter,queueNum,route,customerType,gid
            sim.scheduleEvent(ArrivalEvent(atime,sim,self.groupNum,currentCounter,self.queueNum,self.route,self.customerType,self.gid))



        #Check the queue where this customer was
        #empty queue for counter 0 or 1
        if (counter==0 or counter ==1) and len(sim.states.queue[counter]) == 0:
            print('empty queue for counter 0 or 1')
            sim.states.server_busy_count[counter]=0
        #empty queue for counter 3
        elif counter==3 and len(sim.states.queue[3][self.queueNum])==0 : 
            print('empty queue for counter 3')
            sim.states.server_busy_count[counter] -=1
            sim.states.cashier_busy_count[self.queueNum]=0

        #for not empty queue            
        else: 
            if counter !=2:
                if counter==0 or counter ==1:
                    pop_event=sim.states.queue[counter].pop(0)
                    dtime = self.eventTime + uniform_random(sim.params.st_u[counter][0],sim.params.st_u[counter][1])
                if counter==3:
                    pop_event=sim.states.queue[counter][self.queueNum].pop(0)
                    if self.customerType == 2: #for only drinks customer type
                        dtime = self.eventTime + uniform_random(sim.params.act_u[2][0],sim.params.st_u[2][1])
                    else: 
                        dtime = self.eventTime + uniform_random(sim.params.act_u[2][0],sim.params.st_u[2][1])+uniform_random(sim.params.act_u[self.customerType][0],sim.params.st_u[self.customerType][1])
                
                delay = self.eventTime - pop_event.eventTime
                sim.states.counter_delay[counter]+=delay
                sim.states.customer_delay[pop_event.customerType]+=delay
                sim.states.served_counter[counter]+=1

                sim.scheduleEvent(DepartureEvent(dtime, sim,self.groupNum,self.customerType,self.currentCounter,self.queueNum,self.route,self.gid)) 

                print('departure from not empty queue from counter',counter)



class Simulator:
    def __init__(self, seed):
        self.eventQ = []
        self.simclock = 0
        self.seed = seed
        self.params = None
        self.states = None

    def initialize(self):
        self.simclock = 0
        self.scheduleEvent(StartEvent(0, self))  #starting start event

    def configure(self, params, states):
        self.params = params
        self.states = states 
        for i in range(4):
            self.states.server_busy_count.append(0)
            if i==3:
                for j in range(self.params.employee_count[3]):
                    self.states.cashier_busy_count.append(0)

        for j in range(self.params.employee_count[3]):
            self.states.max_cashier_q_len.append(-math.inf)                

        for i in range(4):
            self.states.queue.append([])
            if  i==3:
                for j in range(self.params.employee_count[i]):
                    self.states.queue[i].append([])   
            else:
                if i != 2: #not applicable for drinks
                    self.params.st_u[i][0]=self.params.st_u[i][0]/self.params.employee_count[i]
                    self.params.st_u[i][1]=self.params.st_u[i][1]/self.params.employee_count[i]

                    self.params.act_u[i][0]=self.params.act_u[i][0]/self.params.employee_count[i]
                    self.params.act_u[i][1]=self.params.act_u[i][1]/self.params.employee_count[i]


    def now(self):
        return self.simclock

    def scheduleEvent(self, event):
        heapq.heappush(self.eventQ, (event.eventTime, event))

    def run(self):
        random.seed(self.seed)
        self.initialize()

        while len(self.eventQ) > 0:
            time, event = heapq.heappop(self.eventQ)

            if event.eventType == 'EXIT':
                print('ExitEvent',event.eventTime)
                break

            if self.states is not None:
                self.states.update(self, event)

            print(event.eventTime, 'Event', event)
            self.simclock = event.eventTime
            event.process(self)

        #print("arrival count ",self.states.ac)
        #print("departure count ",self.states.dc)
        self.states.finish(self)

    def printResults(self):
        self.states.printResults(self)

    def getResults(self):
        #print("hello")
        return self.states.getResults(self)
  


def task_two():
    group_size=[1,2,3,4]
    group_prob=[ 0.5, 0.3, 0.1, 0.1]
    arrival_t=30
    run_time=5400
    routing=[[0,2,3],[1,2,3],[2,3]]
    route_prob=[ 0.80, 0.15,  0.05]
    employee_count=[2,2,0,3]
    st_u=[[50,120],[60,180],[5,20]]
    act_u=[[20,40],[5,15],[5,10]]

    seed = 101
    sim = Simulator(seed)
    sim.configure(Params(group_size,group_prob,arrival_t,run_time,routing,route_prob,employee_count,st_u,act_u), States())
    sim.run()


def main():
    task_two()


if __name__ == "__main__":
    main()
