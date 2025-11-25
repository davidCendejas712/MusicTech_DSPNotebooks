# David Cendejas Rodríguez
# Rafael Vilches Hernández

#%%
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time # para medir tiempos de ejecución

# gráficos en el notebook
%matplotlib inline
SRATE = 44100 # Sample rate, para todo el programa

#%%
def noise1(dur) :
    array = np.empty(int(dur * SRATE))
    for i in range(int(dur * SRATE)):
        array[i] = np.random.uniform(-1, 1)
    print("Ruido1: ", array)
    start = time.time()
    # código ...
    print(f'time: {time.time() - start}')
    return array

def noise2(dur):
    array = np.random.uniform(-1, 1, int(dur*SRATE)) 
    print("Ruido2: ", array)
    start = time.time()
    # código ...
    print(f'time: {time.time() - start}')
    return array


dur = 10

# Plot the data
noise = noise1(dur)
plt.plot(noise[:100])
# título 
plt.title("Ruido")

noise2 = noise2(dur)
plt.plot(noise2[:100])

# mostrar el resultado
plt.show()

sd.play(noise, SRATE)
sd.play(noise2, SRATE)
sd.wait()

#%%

# para que se aprecie en la grafica, poner muy pocos herzios
# para que se escuche, poner 440 herzios

dur = 3   # duración en segundos   
Hz = 440  # frecuencia en Hz

onda = np.arange(int(dur*SRATE))    #crea el array de 0 a dur*SRATE
onda = np.sin(2*np.pi*onda*Hz/SRATE)    #modula la onda

plt.plot(onda)
plt.show()

sd.play(onda, SRATE)
sd.wait()

# %%

#%%

# para que se aprecie en la grafica, poner muy pocos herzios
# para que se escuche, poner 440 herzios

def osc(Hz, dur, amp, phase) :
    onda = np.arange(int(dur*SRATE))    #crea el array de 0 a dur*SRATE
    onda = np.sin(phase+2*np.pi*onda*Hz/SRATE)    #modula la onda
    onda *= amp
    return onda

dur = 3   # duración en segundos   
Hz = 440  # frecuencia en Hz
onda = osc(Hz, dur, 1, 0)

Hz = 220
onda2 = osc(Hz, dur, 1, 0)

plt.plot(onda)
plt.plot(onda2)
plt.show()

sd.play(onda2+onda, SRATE)

sd.wait()

# %%

#lista de tuplas nota, duracion (do, negra)
partitura = [('G', 0.5), ('G', 0.5), ('A', 1), ('G', 1), ('c', 1), ('B', 2), ('C', 1), ('G', 0.5), ('G', 0.5), ('A', 1), ('G', 1), ('d', 0.5), ('c', 2), ('G', 0.5), ('G', 0.5), ('g', 1), ('e',1), ('c', 1), ('B', 1), ('A', 1),('f', 0.5), ('f', 0.5), ('e', 1),('c', 1), ('d', 1), ('c', 2)]

frecs = [523.251, 587.33, 659.255, 698.456, 783.991, 880, 987.767]

ext = [f*2 for f in frecs]
tablaFrecs = frecs + ext
print(tablaFrecs)

notas = "CDEFGABcdefgab"
onda= np.empty(1)
for n in partitura:
    np.concatenate((onda, tablaFrecs[notas.index(n[0])], n[1], 1, 0))



sd.play(onda, SRATE)
sd.wait()


# %%
