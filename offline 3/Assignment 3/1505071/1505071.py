import math
import scipy.stats 
def generateRandom(seed,n):
    Z=[seed]
    U=[]
    U.append(Z[0]/(2**31))
    #print(U[0])
    for i in range(1,n):
        z_i=(65539*Z[i-1])%(2**31)
        u_i=z_i/(2**31)
        #print(u_i)
        U.append(u_i)
        Z.append(z_i)

    #print(U)
    #print(len(U))
    return U


def UniformityTest(n,seed,k,alpha):
    U=generateRandom(seed,n)
    #print(k,alpha)
    dx=float(1.0/k)
    #print("interval range=",dx)
    f=[0 for i in range(k)]
    #print(f)
    #print("\n\n")
    for i in range(n):
        j=math.floor(float(U[i]/dx))
        #print(U[i],j)
        f[j]+=1
    #print("frequency count",f)
    sum=0
    for j in range(k):
        sum+=math.pow((f[j]-float(n/k)),2)
        #print(math.pow((f[j]-float(n/k)),2),sum)

    chi_square=float(k/n)*sum
    q=1-alpha
    df=k-1
    chi_theory=scipy.stats.chi2.ppf(q,df )
    print("k=",k,"chi-squared :",chi_square,"ppf:",chi_theory) 
    if chi_square > chi_theory:
        print("Rejected.\n")
    else:
        print("Accepted.\n")


def serialTest(n,seed,d,k,alpha):
    U_i=generateRandom(seed,n)
    l=math.floor(n/d)  
    #print("Size of tuple:",d)
    #print('number of tuple:',l) 
    U=[[] for i in range(l)]
    #print(U) 
    count=0
    for i in range(l):
        for j in range(d):
            U[i].append(U_i[count])
            count+=1

    #print(U)
    dx=float(1.0/k)
    #print("interval range =",dx)

    f=dict()
    for i in range(l):
        strr='f'
        for j in range(d):
            s= str(math.floor(float(U[i][j]/dx)))
            strr+=s
            #print(s)
        #print(strr)
        if strr in f.keys():
            f[strr]+=1
        else:
            f[strr]=1
    #print(f)

    sum=0
    for key in f.keys():
        sum+=math.pow((f[key]-float(n/(math.pow(k,d)))),2)
    sum+=math.pow((-float(n/(math.pow(k,d)))),2) * (math.pow(k,d)-len(f))
    sum*=float(math.pow(k,d)/n)

    chi_square=sum
    q=1-alpha
    df=math.pow(k,d)-1
    chi_theory=scipy.stats.chi2.ppf(q,df )
    print("d =",d,"k =",k,"chi-squared:",chi_square,"ppf:",chi_theory) 
    if chi_square > chi_theory:
        print("Rejected.\n")
    else:
        print("Accepted.\n")

    pass



def runTest(n,seed,alpha):
    a = [[4529.4, 9044.9, 13568, 18091, 22615, 27892],
        [9044.9, 18097, 27139, 36187, 45234, 55789],
        [13568, 27139, 40721, 54281, 67852, 83685],
        [18091, 36187, 54281, 72414, 90470, 111580],
        [22615, 45234, 67852, 90470, 113262, 139476],
        [27892, 55789, 83685, 111580, 139476, 172860]
    ]
    b = [1 / 6, 5 / 24, 11 / 120, 19 / 720, 29 / 5040, 1 / 840]
    r=[0,0,0,0,0,0]
    U=generateRandom(seed,n)
    #print(U)
    runLen=1
    for i in range(1,n):
        if U[i]>U[i-1]:
            runLen+=1
        else:
            if runLen>=6:
                r[5]+=1
            else:
                r[runLen-1]+=1
            runLen=1
        if i==n-1:
            if runLen>=6:
                r[5]+=1
            else:
                r[runLen-1]+=1


    #print("run length:",r)
    sum=0
    for i in range(6):
        for j in range(6):
            sum+=a[i][j] * (r[i]-n*b[i])* (r[j]-n*b[j] )

    sum =sum/n
    R=sum
    chi_square=R
    q=1-alpha
    df=6
    chi_theory=scipy.stats.chi2.ppf(q,df )
    print("R:",chi_square,"ppf:",chi_theory) 
    if chi_square > chi_theory:
        print("Rejected.\n")
    else: 
        print("Accepted.\n")



def corelationTest(n,seed,j,alpha):
    U=generateRandom(seed,n)
    #print(j)
    h=math.floor((n-1)/j-1)
    #print(h)
    sum=0
    for k in range(h+1):
        sum+=U[k*j] * U[(k+1)*j]
        #print(sum)
    #print("final sum:",sum)
    ro_cap_j=(12/(h+1)) * sum -3
    var_ro_cap_j=(13*h + 7)/math.pow(h+1,2)
    #print("ro_cap_j:",ro_cap_j,"\tvar_ro_cap_j:",var_ro_cap_j)

    A_j=ro_cap_j/math.sqrt(var_ro_cap_j)
    #print("A_j :",A_j)

    z=abs(A_j)
    alpha=1-alpha/2
    z_reject=scipy.stats.norm.ppf(alpha )
    print("j = ",j,"\n|Aj| : ",z,"ppf: ",z_reject) 
    if  z > z_reject:
        print("Rejected.\n")
    else: 
        print("Accepted.\n\n")

    pass


def main():
    seed=1505107
    n=[20,500,4000,10000]
    alpha=0.1

    for i in  range(len(n)):
        print("n=",n[i])
        print(".....................................\nUniformity test\n")
        #uniformity test
        k=[10,20]
        UniformityTest(n[i],seed,k[0],alpha)
        UniformityTest(n[i],seed,k[1],alpha)
        print(".....................................\n")

        print("Serial test\n")
        #serial test
        d=[2,3]
        k=[4,8]
        serialTest(n[i],seed,d[0],k[0],alpha)
        serialTest(n[i],seed,d[0],k[1],alpha)
        serialTest(n[i],seed,d[1],k[0],alpha)
        serialTest(n[i],seed,d[1],k[1],alpha)
        print(".....................................\n")

        print("Run test\n")
        #run test
        runTest(n[i],seed,alpha)
        print(".....................................\n")

        print("Corelation test\n")
        #Corelation test
        j=[1,3,5]
        corelationTest(n[i],seed,j[0],alpha)
        corelationTest(n[i],seed,j[1],alpha)
        corelationTest(n[i],seed,j[2],alpha)
        print(".....................................\n")


    """k=[10,20]
    #UniformityTest(n,seed,k[1],alpha)
    k=[4,8]
    d=[2,3]
    #serialTest(n,seed,d[1],k[1],alpha)
    runTest(10000,seed,alpha)
    j=[1,3,5]
    #corelationTest(n,seed,j[2],alpha)"""
    
if __name__=='__main__':
    main()



    