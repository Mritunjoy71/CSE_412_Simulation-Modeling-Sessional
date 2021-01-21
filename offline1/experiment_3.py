"""
The task is to simulate an M/M/k system with a single queue.
Complete the skeleton code and produce results for three experiments.
The study is mainly to show various results of a queue against its ro parameter.
ro is defined as the ratio of arrival rate vs service rate.
For the sake of comparison, while plotting results from simulation, also produce the analytical results.
"""
import heapq
import random
import math
from lcgrand import *
import matplotlib.pyplot as plt
IDLE = 0
BUSY = 1


def exponential(rate):
    #return random.expovariate(rate)
    return -(1 / rate) * math.log(lcgrand(1))


# Parameters
class Params:
    def __init__(self, lambd, mu, k):
        self.lambd = lambd  # interarrival rate
        self.mu = mu  # service rate
        self.k = k

    # Note lambd and mu are not mean value, they are rates i.e. (1/mean)


# Write more functions if required


# States and statistical counters
class States:
    def __init__(self):
        # States
        self.queue = []
        # Declare other states variables that might be needed
        self.server_status = []
        self.time_last_event = 0.0

        # Statistics
        self.util = 0.0
        self.avgQdelay = 0.0
        self.avgQlength = 0.0
        self.served = 0

        self.total_of_delays = 0.0
        self.area_under_q = 0.0
        self.area_under_busy = 0.0  #area_under_busy_time
        self.num_custs_delayed = 0
        self.total_num_custs = 0
        self.ac = 0
        self.dc = 0
        self.num_in_q = 0

    def update(self, sim, event):
        time_since_last_event = event.eventTime - self.time_last_event
        if sim.isBusy():
            self.area_under_busy += (sim.Busycount()*time_since_last_event)/sim.params.k
        self.area_under_q += (self.num_in_q) * time_since_last_event
        self.time_last_event = event.eventTime

    def finish(self, sim):
        #print("hello")
        try:
            self.avgQdelay = self.total_of_delays / (self.served)
        except ZeroDivisionError:
            print("zero division error .served 0")
        #print(self.area_under_q,self.total_of_delays)    
        self.util = self.area_under_busy / sim.simclock
        self.avgQlength = self.area_under_q / (sim.simclock)

    def printResults(self, sim):
        # DO NOT CHANGE THESE LINES
        print('MMk Results: lambda = %lf, mu = %lf, k = %d' %
              (sim.params.lambd, sim.params.mu, sim.params.k))
        print('MMk Total customer served: %d' % (self.served))
        print('MMk Average queue length: %lf' % (self.avgQlength))
        print('MMk Average customer delay in queue: %lf' % (self.avgQdelay))
        print('MMk Time-average server utility: %lf' % (self.util))

    def getResults(self, sim):
        print(self.avgQlength, self.avgQdelay, self.util)
        return (self.avgQlength, self.avgQdelay, self.util)


# Write more functions if required


class Event:
    def __init__(self, sim):
        self.eventType = None
        self.sim = sim
        self.eventTime = None

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
        atime = self.eventTime + exponential(self.sim.params.lambd)
        sim.scheduleEvent(ArrivalEvent(atime, self.sim))
        sim.scheduleEvent(ExitEvent(10000, self.sim))


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
    def __init__(self, eventTime, sim):
        super().__init__(sim)
        self.eventTime = eventTime
        self.eventType = 'ARRIVAL'
        self.sim = sim

    def process(self, sim):
        # Complete this function
        sim.states.ac += 1
        atime = self.eventTime + exponential(sim.params.lambd)
        sim.scheduleEvent(ArrivalEvent(atime, sim))
        sim.states.total_num_custs += 1
        if sim.isBusy() == BUSY:
            sim.states.queue.append(self.eventTime)
            sim.states.num_in_q += 1
        else:
            delay = 0.0  #since server is not busy ,so no delay
            sim.states.total_of_delays += delay
            #sim.states.server_status = BUSY
            for i in range(sim.params.k):
                if sim.states.server_status[i] == IDLE:
                    sim.states.server_status[i] = BUSY
                    break
            sim.states.served += 1
            dtime = self.eventTime + exponential(sim.params.mu)
            sim.scheduleEvent(DepartureEvent(dtime, sim))


class DepartureEvent(Event):
    # Write __init__ function
    def __init__(self, eventTime, sim):
        super().__init__(sim)
        self.eventTime = eventTime
        self.eventType = 'DEPART'
        self.sim = sim

    def process(self, sim):
        sim.states.dc += 1
        if len(sim.states.queue) == 0:
            #sim.states.server_status = IDLE
            #print("yes")
            for i in range(sim.params.k):
                if sim.states.server_status[i] == BUSY:
                    sim.states.server_status[i] = IDLE
        else:
            #print("yes")
            sim.states.num_in_q -= 1
            delay = self.eventTime - sim.states.queue.pop(0)
            sim.states.total_of_delays += delay
            dtime = self.eventTime + exponential(sim.params.mu)
            sim.scheduleEvent(DepartureEvent(dtime, sim))
            sim.states.served += 1


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
        for i in range(params.k):
            states.server_status.append(IDLE)

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
  

    def isBusy(self):
        isbusy = True
        for i in range(self.params.k):
            if self.states.server_status[i] == IDLE:
                isbusy = False
                break
        return isbusy

    def Busycount(self):
        count = 0
        for i in range(self.params.k):
            if self.states.server_status[i] == BUSY:
                count+=1
        return count 

    def analysis(self):
        averageQlen = (self.params.lambd * self.params.lambd) / (
            self.params.mu * (self.params.mu - self.params.lambd))

        averageDelay_in_q = self.params.lambd / (
            self.params.mu * (self.params.mu - self.params.lambd))

        server_Utilization = self.params.lambd / self.params.mu

        print("\nAnalytical Results :")
        print("lambda = %lf, mu = %lf" % (self.params.lambd, self.params.mu))
        print("Average Queue length", averageQlen)
        print("Average Delay in queue", averageDelay_in_q)
        print("Server Utilization factor", server_Utilization)



def experiment3():
    seed = 101
    lambd = 5.0 / 60
    mu = 8.0 / 60
    k = [u for u in range(1, 11)]

    avglength = []
    avgdelay = []
    util = []

    for ro in k:
        sim = Simulator(seed)
        sim.configure(Params(lambd, mu, ro), States())
        sim.run()

        length, delay, utl = sim.getResults()
        #print(length,delay)
        avglength.append(length)
        avgdelay.append(delay)
        util.append(utl)

    plt.figure(1)
    plt.subplot(311)
    plt.plot(k, avglength)
    plt.xlabel('Num of Server (ro)')
    plt.ylabel('Avg Q length')

    plt.subplot(312)
    plt.plot(k, avgdelay)
    plt.xlabel('Num of Server (ro)')
    plt.ylabel('Avg Q delay (sec)')

    plt.subplot(313)
    plt.plot(k, util)
    plt.xlabel('Num of Server (ro)')
    plt.ylabel('Util')

    plt.show()


def main():
    experiment3()


if __name__ == "__main__":
    main()
