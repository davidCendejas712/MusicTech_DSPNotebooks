
import numpy as np   
import matplotlib.pyplot as plt
from consts import *
from env import *

class ADSR:
    def __init__(self,att,dec,sus,rel):
        self.act = Env([(0,0),(att,1),(att+dec,sus)],xAxis='time')
        self.sus = sus
        self.rel = Env([(0,sus),(rel,0)],xAxis='time')
        self.state = 'off' # act, rel
        self.last = 0

    def next(self):
        if self.state=='off': 
            self.last = 0
            return 0
        elif self.state=='act':             
            out = self.act.next()            
            self.last = out[-1]
            return out
        elif self.state=='rel': 
            out = self.rel.next()   
            self.last = out[-1]
            # cuando se acaba el release pasa a estado off           
            if self.last==0:
                self.state = 'off'            
            return out

    def start(self):
        self.state='act'    
        self.act.reset()

    def release(self):        
        self.rel.reset()
        self.state='rel'    
