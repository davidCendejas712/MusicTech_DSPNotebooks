
import numpy as np   
import matplotlib.pyplot as plt
from consts import *

# Lo mas común es utilizar tiempos en el eje X para definir envolventes
# método para convertir tiempo a frames
def timeToFrame(t): return round(t*SRATE)

class Env:
    # points = [(t0,v0),(t1,v1),(t2,v2),...] valores de la envolvente en instantes de tiempo
    def __init__(self,points,xAxis='samples'):
        if points[0][0]!=0: # el primer tiempo tiene que ser 0
                            # podríamos autocompletar con (0,0) pero mejor dar error
            raise Exception(f'Bad defined env: initial point {points[0]}')

        # si los valores de x están en tiempo traducimos samples
        if xAxis=='time': # si está en frames en vez de tiempo convertimos a tiempos
            points = [(timeToFrame(x),y) for (x,y) in points]

        # construimos la envolvente generando segmentos entre los puntos dados
        self.env = np.zeros(0)        
        (x0,y0) = points[0]  # punto inicial
        for (x,y) in points[1:]:
            self.env = np.concatenate((
                self.env, 
                np.linspace(y0,y,x-x0+1)[:-1] # generamos x-x0+1 puntos y luego descartamos el último 
                ))                            # que vuelve a generarse en el siguiente segmento
                                              # así evitamos "meseta" entre 2 puntos  
            (x0,y0) = (x,y) # nuevo punto de origen
        

        # una vez generada la envolvente, la extendemos hasta completar el último chunk
        # con el último valor self.last: mantiene ese valor hasta el final del chunk
        # Así la longitud de la envolvente es un múltiplo de CHUNK
        # (Esto evita evita errores al multiplicar arrays en numpy)        
        restFrames = CHUNK - (points[-1][0]-points[0][0]) % CHUNK  
        self.env = np.concatenate((self.env, np.full(restFrames,points[-1][1])))        
        #restFrames = CHUNK - (points[-1][0]-points[0][0]) % CHUNK  
        #self.env = np.concatenate((self.env, np.full(restFrames,self.last)))        

        # frame actual 
        self.frame = 0
        
        # la envolvente se extiende indefinidamente con el ultimo valor 
        # no hace falta devolver chunks con ese valor por la sobrecarga del 
        # operador * en numpy: escalar*array o array*array
        self.last = self.env[-1]

    # método next del generador de señal: devuelve array de tamaño CHUNK o valor cte
    def next(self):
        # devolvemos chuncks mientras queda envolvente
        if self.frame<self.env.shape[0]:
            out = self.env[self.frame:self.frame+CHUNK]
            self.frame += CHUNK
            return out
        else: # y la última muestra cuando no quedan
            return np.array([self.last])

    # reseteo del frame en cualquier momento
    # será util después cuando esté sonando una nota y vuelva a lanzarse:
    # se para la envolvente actual y se reinicia
    def reset(self):
        self.frame = 0        
    
