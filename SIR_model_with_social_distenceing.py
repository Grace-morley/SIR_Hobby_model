from matplotlib import pyplot as plt
import numpy as np
from numpy import random as ran



class pandemic_model_with_SD:
    def __init__(self,N,P_tansmition,R_transmition,duration,SD_threshold,SD_tics):
        # set up inital pandemic permaiteras
        self.num_agents=N
        self.P_trans=P_tansmition
        self.R_trans=R_transmition
        self.tic_dration=duration
        self.SD_threshold=SD_threshold
        self.SD_length=SD_tics
        # set up agent positions
        self.positions_x=(ran.rand(1,N))[0]
        self.positions_y=(ran.rand(1,N))[0]
        self.volositis_x=(ran.randn(1,N)*0.0001)[0]
        self.volositis_y=(ran.randn(1,N)*0.0001)[0]
        
        # set up the SIR catigerisation
        self.status=np.asarray(['S']*self.num_agents)
        position_of_infected=ran.randint(0,self.num_agents)
        self.status[position_of_infected]='I'
        self.number_of_days_infected=np.zeros([1,N])[0]
        
        # set up the R number calculation
        self.number_of_agents_infected={position_of_infected:0}
        
        
    def move_one_timestep(self):
        # randomly generate the force the particals feel
        self.forces_x=ran.randn(self.num_agents)*0.0001
        self.forces_y=ran.randn(self.num_agents)*0.0001
        
        # update the volositeies the particals feel based on the new forces 
        self.volositis_x+=self.forces_x
        self.volositis_y+=self.forces_y
        
        # update the positions based on new volosities
        self.positions_x+=self.volositis_x
        self.positions_y+=self.volositis_y
        
        # wrap the positions so the agents are contained in a 1x1 square
        self.positions_x[self.positions_x>1]=0
        self.positions_x[self.positions_x<0]=1
        self.positions_y[self.positions_y>1]=0
        self.positions_y[self.positions_y<0]=1
        
    def social_distence_correction(self):
        
        x_tiled=np.tile(self.positions_x,(self.num_agents,1))\
            -self.positions_x.reshape((-1, 1))
        y_tiled=np.tile(self.positions_y,(self.num_agents,1))\
            -self.positions_y.reshape((-1, 1))
        
        all_rel_r=np.sqrt(x_tiled**2+y_tiled**2)
        
        Kill_self_repushion=range(self.num_agents)
        
        all_rel_r[Kill_self_repushion,Kill_self_repushion]=100
        
        nearest_neighber=np.argmin(all_rel_r,1)
        
        nerest_x_cord=x_tiled[nearest_neighber,Kill_self_repushion]
        nerest_y_cord=y_tiled[nearest_neighber,Kill_self_repushion]
        
        
        hyp=all_rel_r[nearest_neighber,Kill_self_repushion]
        
        X_rasio=nerest_x_cord/hyp
        Y_rasio=nerest_y_cord/hyp
        
        forces=ran.rand(self.num_agents)*0.001
        
        
        self.forces_x=forces*X_rasio+ran.randn(self.num_agents)*0.0001
        self.forces_y=forces*Y_rasio+ran.randn(self.num_agents)*0.0001
        
        self.volositis_x+=self.forces_x
        self.volositis_y+=self.forces_y
        
        self.positions_x+=self.volositis_x
        self.positions_y+=self.volositis_y

        self.positions_x[self.positions_x>1]=0
        self.positions_x[self.positions_x<0]=1
        self.positions_y[self.positions_y>1]=0
        self.positions_y[self.positions_y<0]=1
    
    
    def update_infections(self):
        
        # find the indexes of all the indected agents
        infected_index=[i for i, x in enumerate(self.status) if x=='I']
        #loop over all infected agents 
        for j in infected_index:
            # Find the radi of eavh other agent to the infected agent 
            radious_from_infected=np.sqrt((self.positions_x-\
                self.positions_x[j])**2+(self.positions_y-\
                self.positions_y[j])**2)
                                         
            # find all the agents in range of infection
            range_index=np.where(radious_from_infected<self.R_trans)[0]

            if len(range_index)==0:
                continue
    
            infection_index=list(filter(lambda x: self.status[x]=='S'\
                                        ,range_index))

            if len(infection_index)==0:
                continue
            
            infection_roll=ran.rand(len(infection_index))
            new_infection_radious=[i for i, x in enumerate(infection_roll)\
                                   if x<self.P_trans]
            
            if len(new_infection_radious)==0:
                continue
           
            indexes_to_change=map(infection_index.__getitem__,\
                                  new_infection_radious)

            self.status[list(indexes_to_change)]='I'
        
        infected_index=[i for i, x in enumerate(self.status) if x=='I']
        
        for ii in infected_index:
            self.number_of_days_infected[ii]+=1
            if self.number_of_days_infected[ii]>=self.tic_dration:
                self.status[ii]='R'
        
    def run_sim(self,num_of_tics):
        
        fig=plt.figure()
        ax = fig.add_subplot(211)
        line_S=ax.plot([],[],'g.')[0]
        line_I=ax.plot([],[],'r.')[0]
        line_R=ax.plot([],[],'b.')[0]
        
        ax.set_xlim([0,1])
        ax.set_ylim([0,1])
        
        ax2=fig.add_subplot(212)
        line_S_run=ax2.plot([],[],'g')[0]
        line_I_run=ax2.plot([],[],'r')[0]
        line_R_run=ax2.plot([],[],'b')[0]
        
        S_pop=[]
        I_pop=[]
        R_pop=[]
        t_pop=[]
        
        SD=False
        SD_time=0
        for t in range(num_of_tics):
            S_index=[i for i, x in enumerate(self.status) if x=='S']
            I_index=[i for i, x in enumerate(self.status) if x=='I']
            R_index=[i for i, x in enumerate(self.status) if x=='R']
            
            line_S.set_xdata(self.positions_x[S_index])
            line_S.set_ydata(self.positions_y[S_index])
            
            line_I.set_xdata(self.positions_x[I_index])
            line_I.set_ydata(self.positions_y[I_index])
            
            line_R.set_xdata(self.positions_x[R_index])
            line_R.set_ydata(self.positions_y[R_index])
            
            S_pop.append(len(S_index)/self.num_agents)
            I_pop.append(len(I_index)/self.num_agents)
            R_pop.append(len(R_index)/self.num_agents)
            t_pop.append(t)
            
            #print(S_pop)
            line_S_run.set_ydata(S_pop)
            line_S_run.set_xdata(t_pop)
            line_I_run.set_ydata(I_pop)
            line_I_run.set_xdata(t_pop)
            line_R_run.set_ydata(R_pop)
            line_R_run.set_xdata(t_pop)
            
            ax2.set_xlim([0,t])
            ax2.set_ylim([0,1])
            
            plt.draw()
            plt.pause(0.01)
            
            if len(I_index)/self.num_agents > self.SD_threshold:
                SD=True
            
            if SD==True and SD_time<=self.SD_length:
                self.volositis_x=np.zeros(self.num_agents)
                self.volositis_y=np.zeros(self.num_agents)
                self.social_distence_correction()
                SD_time+=1
            else:
                self.move_one_timestep()
            self.update_infections()