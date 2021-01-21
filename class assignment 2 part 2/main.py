import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.integrate import quad
from tabulate import tabulate

def Normal_Probability_Density_Function(x):
    sigma = 1
    mu = 0
    const = 1.0 / np.sqrt(2*np.pi)
    val=const * np.exp((-(x-mu)**2) / (2.0*(sigma)**2))
    return val

def plotnormal():
    x = np.linspace(-4, 4, num = 100)
    sigma = 1
    mu = 0
    const = 1.0 / np.sqrt(2*np.pi)
    pdf_normal_distribution = const * np.exp((-(x-mu)**2) / (2.0*(sigma)**2))
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(x, pdf_normal_distribution)
    ax.set_ylim(0)
    ax.set_title('Normal Distribution', size = 20)
    ax.set_ylabel('Probability Density', size = 20)
    plt.show()

def main():
    Prob_table = pd.DataFrame(data=[], index = np.round(np.arange(0,3.5,.1),2), columns = np.round(np.arange(0.00,.1,.01),2))
    for row in Prob_table.index:
        for column in Prob_table.columns:
            a = np.round(row+column,2)
            val,none = quad(Normal_Probability_Density_Function, np.NINF,a)
            Prob_table.loc[row] = val
    Prob_table.index=Prob_table.index.astype(str)
    Prob_table.columns= [str(column).ljust(4,'0') for column in Prob_table.columns]
    print(tabulate(Prob_table, headers = 'keys', tablefmt = 'psql')) 
    plotnormal()
if __name__== "__main__":
    main()