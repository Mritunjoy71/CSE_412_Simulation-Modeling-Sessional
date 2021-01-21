#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include<math.h>
#define PI 3.1416
float MonteCarloSim ( float a , float b, int N )
{
    int i;
    float integral = 0;
    float x ;
    for(i=0;i<N;i++)
    {
        x = ((float)rand()/RAND_MAX)*b;
        integral = integral + sin(x);
    }
    integral=integral / N * (b-a);
    return integral;
}

int main() {
   float lo , hi ,res;
   int n;
   lo=0;
   hi=PI/4;
   scanf("%d",&n);
   res = MonteCarloSim(lo,hi,n);
   printf("%f",res);
   return  0;
}
