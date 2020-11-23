from matplotlib import pyplot as plt
import numpy as np
from numpy import random as ran


class smooth_random_movement:
    def __init__(self,N):
        self.N=N
        self.positions_x=ran.rand(1,N)*2-1
        self.positions_y=ran.rand(1,N)*2-1
        self.volositis_x=ran.randn(1,N)*0.001
        self.volositis_y=ran.randn(1,N)*0.001
        
        
    def random_walk(self,ticks):
        fig=plt.figure()
        ax = fig.add_subplot(111)
        line1=ax.plot([],[],'.')[0]
        ax.set_xlim([-1,+1])
        ax.set_ylim([-1,+1])
        for t in range(ticks):
            
            self.forces_x=ran.randn(1,self.N)*0.001
            self.forces_y=ran.randn(1,self.N)*0.001
            self.volositis_x+=self.forces_x
            self.volositis_y+=self.forces_y
            self.positions_x+=self.volositis_x
            self.positions_y+=self.volositis_y
            self.positions_x[self.positions_x>1]=-1
            self.positions_x[self.positions_x<-1]=1
            self.positions_y[self.positions_y>1]=-1
            self.positions_y[self.positions_y<-1]=1
            line1.set_xdata(self.positions_x)
            line1.set_ydata(self.positions_y)
            plt.draw()
            plt.pause(0.1)
            
            
            
som=smooth_random_movement(500)
som.random_walk(400)