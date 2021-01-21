import pandas as pd
import numpy as np
from scipy.stats import norm
from matplotlib import pyplot as plt
def pp_plot(x, dist, line=True, ax=None):
    if ax is None:
        ax = plt.figure().add_subplot(1, 1, 1)
    n = len(x)
    p = np.arange(1, n + 1) / n - 0.5 / n
    pp = np.sort(dist.cdf(x))
    ax.scatterplot(x=p, y=pp, color='blue', edgecolor='blue', ax=ax)
    ax.set_title('PP-plot')
    ax.set_xlabel('Theoretical Probabilities')
    ax.set_ylabel('Sample Probabilities')
    ax.margins(x=0, y=0)
    if line: 
        plt.plot(np.linspace(0, 1), np.linspace(0, 1), 'r', lw=2)
    return ax   
     
data = pd.read_csv('data.csv')
numpy_array = np.genfromtxt("data.csv", delimiter=";", skip_header=1)
print(numpy_array)
p = data['data']
print(p)
parameters = norm.fit(p)
print(parametes)
x = np.linspace(-10,10,100) 
# Generate the pdf (fitted distribution)
fitted_pdf = norm.pdf(x,loc = parameters [0], scale = parameters [1])
# Generate the pdf (normal distribution non fitted)
normal_pdf = norm.pdf(x)
# Type help(plot) for a ton of information on pyplot
plt.plot(x,fitted_pdf,"red",label="Fitted normal dist",linestyle="dashed", linewidth=2)
plt.hist(p,normed=1, bins=20, rwidth=0.65, color="cyan",alpha=.3) #alpha, from 0 (transparent) to 1 (opaque)
plt.title("Normal distribution fitting")
# insert a legend in the plot (using label)
 
fig, ax = plt.subplots(1, 2, figsize=(15, 8)), 
fig.suptitle('PP-plots', fontsize=22)
ax.ProbPlot(rv_norm, scs.norm, loc=0, scale=1).ppplot(line='45', ax=ax[0])
ax[0].set_title('Statsmodels', fontsize=16)
pp_plot(rv_norm, scs.norm(loc=0, scale=1), ax=ax[1])
ax[1].set_title('pp_plot', fontsize=16)
plt.show()
fig, ax = plt.subplots(1, 2, figsize=(15, 8)), 
sm.ProbPlot(rv_skew_norm).qqplot(line='s', ax=ax[0]);
ax[0].set_title('Q-Q plot (vs. Normal)', fontsize=16)
sns.distplot(rv_std_norm, kde=False, norm_hist=True, color='blue', label='Standard Normal', ax=ax[1]) 
sns.distplot(rv_skew_norm, kde=False, norm_hist=True, color='red', label='Skew Normal $\\alpha = 5$', ax=ax[1])
plt.title('Comparison of distributions', fontsize=16)
plt.legend();
plt.show()
