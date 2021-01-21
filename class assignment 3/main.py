import pandas as pd
import numpy as np
from scipy.stats import norm
from matplotlib import pyplot as plt
from scipy.stats import skew 
     
data = pd.read_csv('data.csv')
data_array = np.genfromtxt("data.csv", delimiter=";", skip_header=1)
data_array.sort()
print(data_array)
length=len(data_array)
print('length:',length)
data=data_array
mu1 = np.mean(data)
std1 = np.std(data)
median1=np.median(data)
var1=np.var(data)
co_of_var=std1/mu1
skew1=skew(data)

print('mu1',mu1)
print('standard deviation1',std1)
print('median1',median1)
print('variance1',var1)
print('co efficient of variation',co_of_var)
print('skewness',skew1)

mu, std = norm.fit(data)
print('mu',mu)
print('standard deviation',std1)
pts=data
num_bins = 30
count, bins, ignored = plt.hist(pts, num_bins, density=True,
                                edgecolor='k')
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, mu, std)
q = norm.pdf(x, mu1, std1)
plt.plot(x, p, 'g', linewidth=4)
plt.plot(x, q, 'r', linewidth=1)
title = "Fit results: mu = %.5f,  std = %.5f" % (mu, std)
plt.title(title)

plt.xlabel(r'service time')
plt.ylabel(r'number of occurremce')
plt.show()