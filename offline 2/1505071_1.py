import heapq
import random
#import math
#import numpy as np
from numpy.random import choice
IDLE = 0
BUSY = 1

n=None
n_i=[]
t=None
k=None
p_i=[]
s_i=[]
station_routing=[]
mean_service_time=[]
choice_arr=[]
exit_time=100
def exponential(mean):
    return random.expovariate(1/mean)
    #return random.expovariate(mean/2)+random.expovariate(mean/2)
    #return -(1 / rate) * math.log(lcgrand(1))
def erlang(mean):
    return random.expovariate(1/(mean*2))+random.expovariate(1/(mean*2))

# Parameters
class Params:
    def __init__(self,n,t,k,n_i,p_i,s_i,station_routing,mean_service_time):
        self.lambd =t  # interarrival rate
        self.mu = mean_service_time  # service rate
        self.num_station =n
        self.num_machine=n_i
        self.job_prob=p_i
        self.num_si=s_i
        self.jobs=k
        self.routing=station_routing
        #print('hello from param init')
        #print(self.num_machine)
        #print('mean_service_time in params ',self.mu) 



    # Note lambd and mu are not mean value, they are rates i.e. (1/mean)


# States and statistical counters
class States:
    def __init__(self):
        # States
        self.queue = []
        # Declare other states variables that might be needed
        self.server_busy_count = []
        self.time_last_event = 0.0

        # Statistics
        self.avgQlength =[]
        self.avgQdelay=[]

        self.job_occurance=[]
        self.station_delay=[]
        self.job_delay=[]
        self.station_served=[]
        self.current_jobs=0
        self.area_number_jobs=0
        self.avg_number_jobs=0
        self.avg_job_delay=[]
        self.overall_avg_delay=0
        self.area_number_in_q=[]

    def update(self, sim, event):
        time_since_last_event = event.eventTime - self.time_last_event
        if event.eventType!='START':
            self.area_number_in_q[event.currentStation-1] += len(sim.states.queue[event.currentStation-1]) * time_since_last_event

            self.area_number_jobs += time_since_last_event * self.current_jobs

        self.time_last_event = event.eventTime
        pass



    def finish(self, sim):

        #print("hello")
        
        for i in range(sim.params.num_station):
            try:
                self.avgQdelay[i]=self.station_delay[i]/self.station_served[i]
                self.avgQlength[i] = self.area_number_in_q[i] / (sim.simclock)
            except ZeroDivisionError:
                print("zero division error .served 0")

        self.avg_number_jobs=self.area_number_jobs/sim.simclock

        for i in range(sim.params.jobs):
            try:
                self.avg_job_delay[i]=self.job_delay[i]/self.job_occurance[i]
            except ZeroDivisionError:
                 print("zero division error .job occurance 0")

            self.overall_avg_delay+=sim.params.job_prob[i]*self.avg_job_delay[i]




            
        

    def printResults(self, sim):
        
        print('\navg length in queue')
        for i in range(sim.params.num_station):
            print(self.avgQlength[i])

        print('\navg delay in queue')
        for i in range(sim.params.num_station):
            print(self.avgQdelay[i])

        print('\navg job delay')
        for i in range(sim.params.jobs):
            print(self.avg_job_delay[i])
        print('\navg_number_jobs ',self.avg_number_jobs)
        print('\noverall_avg_delay',self.overall_avg_delay)
        


    def getResults(self, sim):

        #print(self.avgQlength, self.avgQdelay, self.avg_job_delay,self.avg_number_jobs,self.overall_avg_delay)

        return (self.avgQlength, self.avgQdelay, self.avg_job_delay,self.avg_number_jobs,self.overall_avg_delay)


# Write more functions if required


class Event:
    def __init__(self, sim):
        self.eventType = None
        self.sim = sim
        self.eventTime = None
        self.currentStation=None
        self.jobType=None
        self.station_index=None

    def process(self, sim):
        raise Exception('Unimplemented process method for the event!')

    def __repr__(self):
        return self.eventType


class StartEvent(Event):
    def __init__(self, eventTime, sim):
        super().__init__(sim)
        self.eventTime = eventTime
        self.eventType = 'START'
        self.sim = sim
        

    def process(self, sim):
        #jType=sim.params.job_prob.index(max(sim.params.job_prob))
        jType=choice(choice_arr,p=p_i)
        #print('from start event process job type',jType)
        current_station=sim.params.routing[jType][0]
        #print('from start event process current_station',current_station)
        station_index=0
        atime = self.eventTime + exponential(self.sim.params.lambd)
        sim.scheduleEvent(ArrivalEvent(atime, self.sim,jType,current_station,station_index))
        sim.scheduleEvent(ExitEvent(8, self.sim))


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
    def __init__(self, eventTime, sim,jType,current_station,station_index):
        super().__init__(sim)
        self.eventTime = eventTime
        self.eventType = 'ARRIVAL'
        self.sim = sim
        self.currentStation=current_station
        self.jobType=jType
        self.station_index=station_index

    def process(self, sim):
        # Complete this function
        if self.station_index==0:

            sim.states.job_occurance[self.jobType]+=1
            sim.states.current_jobs+=1

            jType=choice(choice_arr,p=p_i)
            #print('from arrival event process job type',jType)
            current_station=sim.params.routing[jType][0]
            #print('from arrival event process current_station',current_station)
            station_index=0
            atime = self.eventTime + exponential(self.sim.params.lambd)
            sim.scheduleEvent(ArrivalEvent(atime, sim,jType,current_station,station_index))

        #sim.states.total_num_custs += 1
        if sim.isBusy(self.currentStation) == BUSY:
            sim.states.queue[self.currentStation-1].append(self)

        else:
            sim.states.server_busy_count[self.currentStation-1]+=1

            sim.states.station_served[self.currentStation-1] +=1

            dtime = self.eventTime + erlang(sim.params.mu[self.jobType][self.station_index])
            sim.scheduleEvent(DepartureEvent(dtime, sim,self.jobType,self.currentStation,self.station_index))


class DepartureEvent(Event):
    # Write __init__ function
    def __init__(self, eventTime, sim,jType,current_station,station_index):
        super().__init__(sim)
        self.eventTime = eventTime
        self.eventType = 'DEPART'
        self.sim = sim
        self.jobType=jType
        self.currentStation=current_station
        self.station_index=station_index

    def process(self, sim):
        if self.station_index ==(sim.params.num_si[self.jobType]-1):
            sim.states.current_jobs-=1
        else:    
            jType=self.jobType
            #print('from arrival event process job type',jType)
            station_index=self.station_index+1
            current_station=sim.params.routing[jType][station_index]
            #print('from arrival event process current_station',current_station)
            atime = self.eventTime 
            sim.scheduleEvent(ArrivalEvent(atime, sim,jType,current_station,station_index))

        if len(sim.states.queue[self.currentStation-1]) == 0:
            #print("yes")
            sim.states.server_busy_count[self.currentStation-1] -=1
            
        else:
            #print("departure else")
        
            pop_event=sim.states.queue[self.currentStation-1].pop(0)

            delay = self.eventTime - pop_event.eventTime
            sim.states.station_delay[self.currentStation-1]+=delay
            sim.states.job_delay[self.jobType]+=delay

            dtime = self.eventTime + erlang(sim.params.mu[pop_event.jobType][pop_event.station_index])
            sim.scheduleEvent(DepartureEvent(dtime, sim,pop_event.jobType,pop_event.currentStation,pop_event.station_index))

            sim.states.station_served[self.currentStation-1]+=1



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
        #print('hello')
        #print(self.params.num_station)

        for i in range(self.params.num_station):

            self.states.avgQlength.append(0)
            self.states.avgQdelay.append(0)
            self.states.station_served.append(0)
            self.states.station_delay.append(0)
            self.states.queue.append([])
            self.states.area_number_in_q.append(0)
            #print('hello2')
            self.states.server_busy_count.append(0)

        #print('server busy count ',self.states.server_busy_count)   
        
        for i in range(self.params.jobs):
            self.states.avg_job_delay.append(0) 
            self.states.job_occurance.append(0) 
            self.states.job_delay.append(0)
        #print('job_occurance ',self.states.job_occurance)

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
                break

            if self.states is not None:
                self.states.update(self, event)

            #print(event.eventTime, 'Event', event)
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
  

    def isBusy(self,current_station):
        isbusy=False
        #print('is busy ',current_station)
        if self.states.server_busy_count[current_station-1] >=self.params.num_machine[current_station-1]:
            isbusy=True
        return isbusy



def take_input():
    global n
    global n_i
    global t
    global k
    global p_i
    global s_i
    global station_routing
    global mean_service_time
    global choice_arr

    file=open('input.txt')
    lines=file.readlines()
    line_count=0
    flag=True
    for line in lines:
        if line_count==0:
            n=int(line)
            print(n)
        if line_count==1:
            var=line.split()
            for v in var:
                n_i.append(int(v))
                #print(v)
            print(n_i)    
        if line_count==2:
            t=float(line)
            print(t)  
        if line_count==3:
            k=int(line)
            for i in range(k):
                choice_arr.append(i)

            print(k)  
        if line_count==4: 
            var=line.split()
            for v in var:
                p_i.append(float(v))
                #print(v)
            print(p_i)    
        if line_count==5: 
            var=line.split()
            for v in var:
                s_i.append(int(v))
                #print(v)
            print(s_i)    
        if line_count >5:
            if flag==True:
                flag=False
                var=line.split()
                r=[]
                for v in var:
                    r.append(int(v))
                station_routing.append(r)
                print(r)
            else:
                flag=True
                var=line.split()
                mst=[]
                for v in var:
                    mst.append(float(v))
                mean_service_time.append(mst)
                print(mst)
        line_count+=1

    #print('station_routing ',station_routing)
    #print('mean_service_time ',mean_service_time)    
    pass



def task_one():

    Qlength=[]
    Qdelay=[]
    job_delay=[]
    number_jobs=[]
    overall_delay=[]
    Exit_time=8
    for i in range(30):
        seed = 101
        sim = Simulator(seed)
        sim.configure(Params(n,t,k,n_i,p_i,s_i,station_routing,mean_service_time), States())
        sim.run()

        avgQlength,avgQdelay,avg_job_delay,avg_number_jobs,overall_avg_delay=sim.getResults()
        Qlength.append(avgQlength)
        Qdelay.append(avgQdelay)
        job_delay.append(avg_job_delay)
        number_jobs.append(avg_number_jobs)
        overall_delay.append(overall_avg_delay)

        
        #sim.printResults()

    aQlength=[]
    aQdelay=[]
    ajob_delay=[]
    anumber_jobs=0
    aoverall_delay=0   
    for i in range(n):   
        length=0
        delay=0
        for j in range(30):
            length+=Qlength[j][i]
            delay+=Qdelay[j][i]
        aQlength.append(length)
        aQdelay.append(delay)

    for i in range(n):   
       aQlength[i]=aQlength[i]/30.0
       aQdelay[i]= aQdelay[i]/30.0  

    for i in range(k):   
        delay=0
        for j in range(30):
            delay+=job_delay[j][i]
        ajob_delay.append(delay)  

    for i in range(k):
        ajob_delay[i]=ajob_delay[i]/30.0      

    for j in range(30):
        anumber_jobs+=number_jobs[j]
        aoverall_delay+=overall_delay[j]

    anumber_jobs=anumber_jobs/30.0
    aoverall_delay=aoverall_delay/30.0   



    print('\nstation no.\t\tavg length in queue\t\tavg delay in queue')
    for i in range(n):
        print(i+1,'\t\t\t',aQlength[i],'\t\t\t',aQdelay[i])


    print('\nJob No.\t\tavg job delay')
    for i in range(k):
        print(i+1,'\t\t\t',ajob_delay[i])
    print('\navg_number_jobs :',anumber_jobs)
    print('\noverall_avg_delay :',aoverall_delay) 

    


def main():
    take_input()
    task_one()


if __name__ == "__main__":
    main()
