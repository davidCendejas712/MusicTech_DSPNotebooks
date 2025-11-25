# David Cendejas Rodríguez
# Rafael Vilches Hernández

#%%
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time # para medir tiempos de ejecución

# gráficos en el notebook
#%matplotlib inline
SRATE = 44100 # Sample rate, para todo el programa

#%%
# EJERCICIO 1 : Generar ruido blanco
#Ruido blanco creado no eficientemente (sin usar numpy)
def noise1(dur) :
    array = np.empty(int(dur * SRATE))
    for i in range(int(dur * SRATE)):
        array[i] = np.random.uniform(-1, 1)
    print("Ruido1: ", array)
    start = time.time()
    print(f'time: {time.time() - start}')
    return array

#Ruido blanco creado con numpy
def noise2(dur):
    array = np.random.uniform(-1, 1, int(dur*SRATE)) 
    print("Ruido2: ", array)
    start = time.time()
    print(f'time: {time.time() - start}')
    return array

dur = 5    # duración en segundos

noise = noise1(dur)

plt.plot(noise[:100])
plt.title("Ruido")

noise2 = noise2(dur)
plt.plot(noise2[:100])

plt.show()

sd.play(noise, SRATE)
sd.play(noise2, SRATE)
sd.wait()

#%%
# EJERCICIO 2 : Crear una onda sinusoidal 

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

#%%
# EJERCICIO 3 : Implementar funcion osc()

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
# EJERCICIO 4 EVALUABLE : Dada una partitura, tocar la canción

#lista de tuplas nota, duracion (do, negra)
partitura = [('G', 0.5), ('G', 0.5), ('A', 1), ('G', 1), ('c', 1), ('B', 2), ('C', 1), ('G', 0.5), ('G', 0.5), ('A', 1), ('G', 1), ('d', 0.5), ('c', 2), ('G', 0.5), ('G', 0.5), ('g', 1), ('e',1), ('c', 1), ('B', 1), ('A', 1),('f', 0.5), ('f', 0.5), ('e', 1),('c', 1), ('d', 1), ('c', 2)]

#lista de frecuencias de las notas
frecs = [523.251, 587.33, 659.255, 698.456, 783.991, 880, 987.767]

#extensión de la lista de frecuencias para las octavas superiores
ext = [f*2 for f in frecs]

tablaFrecs = frecs + ext
print(tablaFrecs)

notas = "CDEFGABcdefgab"   # notas.index() devuelve la posición de la nota en la lista, para buscar la frecuencia

onda= np.empty(1) 

for n in partitura:
    # en vez de hacer sd.wait() al final de cada nota, se concatenan las ondas
    onda = np.concatenate((onda, osc(tablaFrecs[notas.index(n[0])], n[1]*0.5, 0.2, 0)))

sd.play(onda, SRATE)
sd.wait()

#%%
#EJERCICIO 5 : Implementar un modulador: oscilador entre dos valores [v0,v1] con 0<=v0<v1<=1

def moduladora(frec,dur,v0,v1):
    o = osc(frec,dur,1,0)
    return ((v1-v0)*o+ (v1+v0))/2

m = moduladora(3,2,0.5,0.8)

plt.plot(m)

#%%
#EJERCICIO 6 EVALUABLE : implementar una función harmOsc, para simular un nota con sus armónicos

def harmOsc(f,amps,dur,amp):
    armonico = 1
    onda = np.zeros(int(SRATE*dur))
    for am in amps:  #amps = lista de amplitudes de los armonicos
        onda+= osc(armonico*f,dur,am,0)
        armonico+=1
        pass
    return onda*amp

amps = np.array([1, 0.9, 0.7, 0.6, 0.4, 0.3]) #Piano

# Para cada nota, se reproduce la onda con armónicos corresponidentes al piano
for fr in range(7):
    sd.play(harmOsc(frecs[fr],amps,0.4,0.2))
    sd.wait()

sd.wait()


# %%
#EJERCICIO 7 : Con la misma idea que el oscilador osc que hemos visto, implementar funciones saw, square, triangle

def saw(frec,dur,amp,phase):
    onda = np.arange(int(dur*SRATE))
    onda = np.mod(onda,SRATE/frec)
    onda = onda/(SRATE/frec)
    onda = 2*onda-1
    onda = onda*amp
    return onda

def square(frec,dur,amp,phase):
    onda = np.arange(int(dur*SRATE))
    onda = np.mod(onda,SRATE/frec)
    onda = onda/(SRATE/frec)
    onda = np.sign(onda-0.5)
    onda = onda*amp
    return onda

def triangle(frec,dur,amp,phase):
    onda = np.arange(int(dur*SRATE))
    onda = np.mod(onda,SRATE/frec)
    onda = onda/(SRATE/frec)
    onda = 2*np.abs(onda-0.5)
    onda = 2*onda-1
    onda = onda*amp
    return onda

plt.plot(saw(50,0.1,1,0))
plt.plot(square(50,0.1,1,0))
plt.plot(triangle(50,0.1,1,0))
plt.show()

sd.play(saw(440,2,0.5,0))
sd.wait()
sd.play(square(440,2,0.5,0))
sd.wait()
sd.play(triangle(440,2,0.5,0))
sd.wait()

# %%
# EJERCICIO 8 : Implementar una función fadeOut(sample,t) y fadeIn(sample,t), desde t hasta el final

def fadeOut(sample,t):
    return sample*(1-np.linspace(0,1,len(sample))**t)

def fadeIn(sample,t):   
    return sample*(np.linspace(0,1,len(sample))**t)

onda = osc(440,2,1,0)
plt.plot(onda)
onda = fadeOut(onda,2)
plt.plot(onda)

sd.play(onda,SRATE)
sd.wait()

onda = osc(440,2,1,0)
onda = fadeIn(onda,2)
plt.plot(onda)

sd.play(onda,SRATE)
sd.wait()

# %%
# EJERCICIO 9 : Implementar una función env(attack,release) que genere una envolvente y playNote que toque una nota 
def env(attack,release):
    return np.concatenate([np.linspace(0,1,int(SRATE*attack)),np.linspace(1,0,int(SRATE*release))])

enve = env(0.05,1)
plt.plot(enve)

dur = 1
attack = 0.05
onda = osc(440,2,1,0)
enve = np.pad(enve, (0, len(onda) - len(enve)), 'constant')   # se añaden ceros al final de la envolvente
onda = onda*enve

plt.plot(onda)
sd.play(onda,SRATE)
sd.wait()

def playNote(freq,dur,amp,attack,decay):
    onda = osc(freq,dur,amp,0)
    enve = env(attack,decay)
    if len(onda) > len(enve) :
        enve = np.pad(enve, (0, len(onda) - len(enve)), 'constant')
    else :
        onda = np.pad(onda, (0, len(enve) - len(onda)), 'constant')
    onda = onda*enve
    sd.play(onda,SRATE)
    sd.wait()
    

playNote(440,2,0.5,0.05,1)
sd.wait()

# %%
# EJERCICIO 10 : Implementar una función playSong que toque una canción con envolventes

def playSong(song):
    for n in song:
        playNote(tablaFrecs[notas.index(n[0])],n[1],0.2,0.05,1)

#Suena a trompicones porque no se hace el concatenate
playSong(partitura)

# %%
