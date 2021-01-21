#_____Random number generation with poisson distribution_____#

import numpy as np
import math 
import matplotlib.pyplot as plt
np.random.seed(41)
n=100
random_numbers=[]
for i in range(n):
  counter=0
  x1=1
  while(True):
    x2=np.random.uniform()
    if x1*x2 < math.exp(-1):
      random_numbers.append(counter)
      break
    else:
      x1=x2
      counter+=1  
      #print(counter)

#print(random_numbers)

count, bins, ignored = plt.hist(random_numbers, 14, density=False)
plt.show()

numbers_raito=[]
for i in range(n):
  numbers_raito.append(random_numbers[i]/n)

plt.autoscale() 
count, bins, ignored = plt.hist(numbers_raito, 14, density=True) 
#plt.show()

probability=[]

for i in range(n):
  a=random_numbers[i]
  b=math.exp(-1)*math.pow(1,a)/math.factorial(a)
  probability.append(b)


plt.autoscale() 
count, bins, ignored = plt.hist(probability, 14, density=False) 
#plt.show()

