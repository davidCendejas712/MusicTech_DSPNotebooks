#%%
# David Cendejas Rodríguez
# Rafael Vilches Hernández
import numpy as np         
import sounddevice as sd  
import matplotlib.pyplot as plt
import tkinter             
# EJERCICIO 1 EVALUABLE : Implementar Osc y Modulator, pero esta vez por chunks
CHUNK = 1024
SRATE = 48000

class Osc:
    def __init__(self,freq=440.0,amp=1.0,phase=0.0):
        self.freq = freq
        self.amp = amp
        self.phase = phase
        self.frame = 0 # frame inicial

    def next(self):    
        out = self.amp*np.sin(2*np.pi*(np.arange(self.frame,self.frame+CHUNK))*self.freq/SRATE+self.phase)
        
        self.frame += CHUNK # actualizamos el frame
        return out
    
class Modulator:
    def __init__(self,signal,freq,v0,v1):
        self.freq = freq
        self.signal = signal
        self.v0 = v0
        self.v1 = v1
        self.frame = 0 # frame inicial

        self.mod = Osc(freq=freq)

    def next(self):    
        out = self.signal.next()* (self.v0 + ((self.v1-self.v0) * (0.5+(self.mod.next()/2))))
        
        self.frame += CHUNK # actualizamos el frame
        return out
    
# PRUEBA
# señal que vamos a modular
signal = Osc()
# con un modulador de 2 Hz y amplitud en [0.2,0.9]
mod = Modulator(signal,freq=2,v0=.2,v1=.9)
# generamos 1.5 segundos de señal modulada
time = 1.5
chunks = int(time*SRATE/CHUNK) # número de chunks a generar
signal = np.empty(0) # acumulador de la señal
for i in range(chunks): # generamos los chunks
    signal = np.append(signal,mod.next())
plt.plot(signal)
sd.play(signal)
sd.wait()

# %%
# EJERCICIO 3 EVALUABLE : Extender la clase oscFM del notebook con Tkinter para modificar la frecuencia moduladora y el índice Beta

class OscFM:
    def __init__(self,fc=110.0,amp=1.0,fm=6.0, beta=1.0):
        self.fc = fc
        self.amp = amp
        self.fm = fm
        self.beta = beta
        self.frame = 0

        # moduladora = βsin(2πfm)
        self.mod = Osc(freq=fm,amp=beta)
        
    def next(self):  
        # sin(2πfc+mod)  
        # sacamos el siguiente chunk de la moduladora
        mod = self.mod.next()

        # soporte para el chunk de salida
        sample = np.arange(self.frame,self.frame+CHUNK)        
        # aplicamos formula
        out =  self.amp*np.sin(2*np.pi*self.fc*sample/SRATE + mod)
        self.frame += CHUNK
        return out 
    
    def getMod(self):
        return self.fm
    def setMod(self, newFM):
        self.fm=newFM
        self.mod = Osc(freq=newFM,amp=self.beta)
    def getBeta(self):
        return self.beta
    def setBeta(self, newBeta):
        self.beta=newBeta
        self.mod = Osc(freq=self.fm,amp=newBeta)
    # como suena?

input = OscFM()

def callback(outdata, frames, time, status):
    if status: print(status)
    if input:    
        s = input.next()
        s = np.float32(s)
    else:
        s = np.zeros(CHUNK,dtype=np.float32)
    outdata[:] = s.reshape(-1, 1)

# stream de salida con callBack
stream = sd.OutputStream(samplerate=SRATE, callback=callback, blocksize=CHUNK)
stream.start()

# Se crea la ventana de control
root = tkinter.Tk()
text = tkinter.Text(root,height=6,width=60)
text.pack(side=tkinter.BOTTOM)
text.insert(tkinter.INSERT,"Press 'b' to reduce Beta, B to augment\n")
text.insert(tkinter.INSERT,"Press 'm' to reduce modFrec, M to augment\n")

# call back para la pulsación de teclas
def key_down(event):
    global input  # conexión con sounddevice
    if event.char=='b': 
        print('beta reduced')
        input.setBeta(input.getBeta()-1)  # enrutamos la señal de la nota al "input" del stream
    elif event.char=='B': 
        print('beta augmented')
        input.setBeta(input.getBeta()+1)
    elif event.char=='M': 
        print('modFrec augmented')
        input.setMod(input.getMod()+1)
    elif event.char=='m': 
        print('modFrec reduced')
        input.setMod(input.getMod()-1)
    

# enlace de la pulsación de teclas con la función key_down
text.bind('<Key>', key_down)

# arrancamos todo!!
root.mainloop()
# ejecución bloqueada hasta que se cierre ventana

# limpieza..
stream.stop()
stream.close()
stream.stop() 

#%%
# EJERCICIO 4 EVALUABLE : efecto de modulación de paneo (o balance de canales)
class PanningModulator:
    def __init__(self, signal, freq):
        self.signal = signal
        self.mod = Osc(freq=freq)

    def next(self):
        p = 0.5 * (1 + self.mod.next())  # Modulación de paneo en el rango [0, 1]
        left_amp = np.sqrt(1 - p)
        right_amp = np.sqrt(p)
        signal_chunk = self.signal.next()
        left = signal_chunk * left_amp
        right = signal_chunk * right_amp
        return np.column_stack((left, right))

# PRUEBA
# señal que vamos a modular
signal = Osc()
# con un modulador de paneo de 0.5 Hz
panning_mod = PanningModulator(signal, freq=0.5)
# generamos 1.5 segundos de señal modulada
time = 3
chunks = int(time * SRATE / CHUNK)  # número de chunks a generar
stereo_signal = np.empty((0, 2))  # acumulador de la señal estéreo
for i in range(chunks):  # generamos los chunks
    stereo_signal = np.append(stereo_signal, panning_mod.next(), axis=0)

plt.plot(stereo_signal)
sd.play(stereo_signal, SRATE)
sd.wait()

#%%
#EJERCICIO 5 :


# %%
# EJERCICIO 7 EVALUABLE : Implementar un Delay
class Delay:
    def __init__(self, time):
        self.time = time
        pass
    def next(self, signal):
        buffer = np.zeros(time*SRATE)
        return np.append(signal,buffer)
    

#%%
# EJERCICIO 8 EVALUABLE : Implementar un Theremin
import numpy as np
import sounddevice as sd
import tkinter as tk

CHUNK = 1024
SRATE = 48000
WIDTH, HEIGHT = 800, 600

class ThereminOsc:
    def __init__(self, freq=440.0, amp=1.0):
        self.freq = freq
        self.amp = amp
        self.frame = 0

    def set_freq(self, freq):
        self.freq = freq

    def set_amp(self, amp):
        self.amp = amp

    def next(self):
        t = (np.arange(self.frame, self.frame + CHUNK) / SRATE).reshape(-1, 1)
        self.frame += CHUNK
        return self.amp * np.sin(2 * np.pi * self.freq * t)

# Crear el oscilador del theremin
theremin = ThereminOsc()

# Callback para la reproducción de audio
def audio_callback(outdata, frames, time, status):
    if status:
        print(status)
    outdata[:] = theremin.next()

# Crear el stream de salida con el callback
stream = sd.OutputStream(samplerate=SRATE, blocksize=CHUNK, dtype='float32', channels=1, callback=audio_callback)
stream.start()

# Crear la interfaz gráfica con Tkinter
root = tk.Tk()
root.geometry(f"{WIDTH}x{HEIGHT}")

def motion(event):
    x = root.winfo_pointerx() - root.winfo_rootx()
    y = root.winfo_pointery() - root.winfo_rooty()
    freq = 50 + (x / WIDTH) * 1450  # Rango de frecuencia [50, 1500] Hz
    amp = 1 - (y / HEIGHT)  # Rango de amplitud [0, 1]
    theremin.set_freq(freq)
    theremin.set_amp(amp)
    print(f'Freq: {freq:.2f} Hz, Amp: {amp:.2f}')

root.bind('<Motion>', motion)
root.mainloop()

# Detener el stream al cerrar la ventana
stream.stop()
stream.close()
# %%
