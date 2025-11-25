
import numpy as np    
import matplotlib.pyplot as plt
from tkinter import *

class Slider:
    def __init__(self,tk,name='a',ini=0.2,from_=0.0,to=1.0,step=0.1,orient=HORIZONTAL,packSide=TOP):
        self.val = DoubleVar() # para guardar y modificar el valor del parámetro en cuestión
        self.val.set(ini)
                
        self.scale = Scale(tk, label=name,
            from_=from_, to=to, resolution=step, 
            orient=orient, width=30,sliderlength=10, length=300, bd=6,
            variable = self.val)
            
        self.scale.pack(side=packSide)

    def get(self):
        return self.val.get()
