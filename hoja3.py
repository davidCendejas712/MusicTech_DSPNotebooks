#%%
#EJERCICIO 1 EVALUABLE : 
# Extender el instrumento FM presentado en clase de modo que permita seleccionar el tipo de onda (sinosuoidal, cuadrada, triangular,
# diente de sierra) tanto para la portadora fc como para la moduladora fm. Añadir a la interface gráfica dos ComboBox de TkInter 
# para mostrar las opciones para cada entrada.

# Para la FC: Se modifica la clase SynthFm y OscFM para que tenga en cuenta la forma de la onda ya que Instrument -> SynthFM -> OscFM
# Para la FM: Se modifica la clase Osc
# Como voy a modificarlas, las copio aquí para evitar confusión

# Cada boton cambia la forma de la onda de la portadora y de la moduladora, se añaden 4 botones para cada una de las formas de onda
# Creo está correcto así, pero suena horrible :c

import numpy as np   
import matplotlib.pyplot as plt
from consts import *
from tkinter import *
from slider import *
from adsr import *
import scipy.signal as sg 

class Osc:
    def __init__(self,freq=440.0,amp=1.0,phase=0.0, shape = 'sin'):
        self.freq = freq
        self.amp = amp
        self.phase = phase
        self.frame = 0
        self.shape = shape

    def next(self):    
        if self.shape=='sin':
            out = np.sin(2*np.pi*(np.arange(self.frame,self.frame+CHUNK))*self.freq/SRATE+self.phase)
        elif self.shape=='square':
            out = sg.square(2*np.pi*(np.arange(self.frame,self.frame+CHUNK))*self.freq/SRATE+self.phase)
        elif self.shape=='sawtooth':
            out = sg.sawtooth(2*np.pi*(np.arange(self.frame,self.frame+CHUNK))*self.freq/SRATE+self.phase)
        elif self.shape=='triangle':
            # Ojo, la triangular no existe como tal en scipy, pero podemos hacerla con dos sawtooth
            # el 2º parametro define la "rampa" la subida y bajada (ver documentacion)
            out = sg.sawtooth(2*np.pi*(np.arange(self.frame,self.frame+CHUNK))*self.freq/SRATE+self.phase,0.5)
        self.frame += CHUNK
        return out

class OscFM:
    def __init__(self,phase=0,fc=110.0,amp=1.0,fm=6.0, beta=1.0, shape = 'sin', shapeM = 'sin'):
        self.fc = fc
        self.amp = amp
        self.fm = fm
        self.beta = beta
        self.frame = 0
        self.shape = shape
        self.shapeM = shapeM 
        self.phase = phase
        # moduladora = βsin(2πfm)
        self.mod = Osc(freq=fm,amp=beta, shape = self.shapeM)  # MODIFICACION FM !!!
        
    def next(self):  
        mod_signal = self.mod.next()
        if self.shape=='sin':
            out = np.sin(2*np.pi*(np.arange(self.frame,self.frame+CHUNK))*self.fc/SRATE+self.phase + mod_signal)
        elif self.shape=='square':
            out = sg.square(2*np.pi*(np.arange(self.frame,self.frame+CHUNK))*self.fc/SRATE+self.phase + mod_signal)
        elif self.shape=='sawtooth':
            out = sg.sawtooth(2*np.pi*(np.arange(self.frame,self.frame+CHUNK))*self.fc/SRATE+self.phase + mod_signal)
        elif self.shape=='triangle':
            # Ojo, la triangular no existe como tal en scipy, pero podemos hacerla con dos sawtooth
            # el 2º parametro define la "rampa" la subida y bajada (ver documentacion)
            out = sg.sawtooth(2*np.pi*(np.arange(self.frame,self.frame+CHUNK))*self.fc/SRATE+self.phase + mod_signal,0.5)
        self.frame += CHUNK
        return out 

    def setBeta(self,beta):
        self.beta = beta
        self.mod.amp = beta

    def setFm(self,fm):
        self.fm = fm
        self.mod.freq = fm

    def getBeta(self):
        return self.beta    

    def getFm(self):
        return self.fm


class SynthFM:
    def __init__(self,
                fc=110,amp=1.0,ratio=0.5, beta=5.0,   # parámetros del generador FM
                attack=0.01,decay=0.02, sustain=0.3,release=1.0, shape = 'sin', shapeM = 'sin'): # parámetros del ADSR        
        self.fc = fc
        self.amp =  amp
        self.ratio = ratio
        self.fm = self.ratio*self.fc # fm en función de fc y ratio
        self.beta = beta
        self.shape = shape
        self.shapeM = shapeM 

        self.signal = OscFM(self.fc,amp=self.amp,fm=self.fm,beta=self.beta, shape = self.shape, shapeM = self.shapeM) # generador  #MODIFICACION FC !!!
        self.adsr = ADSR(attack,decay,sustain,release)  # envolvente adsr

        # se dispara automáticamente
        self.state = 'on' # activo
        self.adsr.start() # adsr activa

    def start(self):
        self.adsr.start()

    # siguiente chunk del generador
    def next(self): 
        out = self.signal.next()*self.adsr.next()
        if self.adsr.state=='off': # cuando acaba el adsr por completo (incluido el release)
            self.state = 'off'     # el sinte tb acaba de producir señal
        return out     
    
    # el noteOff del sinte activa el release del ADSR
    def noteOff(self):
        #print('release')
        self.adsr.release()

    def setAmp(self,val): 
        self.amp = val 

    def setFm(self,val): 
        self.fm = val  

    def setBeta(self,val): 
        self.beta = val


class InstrumentNew1:
    def __init__(self,tk,name="FM synthetizer",amp=0.2,ratio=3,beta=0.6,shape='sin',shapeM='sin'): 
        self.shape = shape
        self.shapeM = shapeM
        frame = LabelFrame(tk, text=name, bg="#808090")
        frame.pack(side=LEFT)
        # Synth params con sus sliders
        frameOsc = LabelFrame(frame, text="FM oscillator", bg="#808090")
        frameOsc.pack(side=LEFT, fill="both", expand="yes")
        
        self.ampS = Slider(frameOsc,'amp',packSide=TOP,
                           ini=amp,from_=0.0,to=1.0,step=0.05) 

        self.ratioS = Slider(frameOsc,'ratio',packSide=TOP,
                           ini=ratio,from_=0.0,to=20.0,step=0.5)
    
        self.betaS = Slider(frameOsc,'beta',packSide=TOP,
                            ini=beta,from_=0.0,to=10.0,step=0.05) 
        
        # una ventana de texto interactiva para poder lanzar notas con el teclado del ordenador
        text = Text(frameOsc,height=4,width=40)
        text.pack(side=BOTTOM)
        text.bind('<KeyPress>', self.down)
        text.bind('<KeyRelease>', self.up)

        # Crear botones para seleccionar la forma de onda Fc
        self.buttonSin = Button(frameOsc, text="SIN", command=lambda: self.set_waveform('sin'))
        self.buttonTri = Button(frameOsc, text="TRI", command=lambda: self.set_waveform('triangle'))
        self.buttonSaw = Button(frameOsc, text="SAW", command=lambda: self.set_waveform('sawtooth'))
        self.buttonSqu = Button(frameOsc, text="SQU", command=lambda: self.set_waveform('square'))
        
        # Crear botones para seleccionar la forma de onda Fm
        self.buttonSinM = Button(frameOsc, text="SIN m", command=lambda: self.set_waveformM('sin'))
        self.buttonTriM = Button(frameOsc, text="TRI m", command=lambda: self.set_waveformM('triangle'))
        self.buttonSawM = Button(frameOsc, text="SAW m", command=lambda: self.set_waveformM('sawtooth'))
        self.buttonSquM = Button(frameOsc, text="SQU m", command=lambda: self.set_waveformM('square'))

        # Empaquetar los botones
        self.buttonSin.pack(side=LEFT)
        self.buttonTri.pack(side=LEFT)
        self.buttonSaw.pack(side=LEFT)
        self.buttonSqu.pack(side=LEFT)
        self.buttonSinM.pack(side=LEFT)
        self.buttonTriM.pack(side=LEFT)
        self.buttonSawM.pack(side=LEFT)
        self.buttonSquM.pack(side=LEFT)

        # ADSR params con sus sliders
        frameADSR = LabelFrame(frame, text="ADSR", bg="#808090")
        frameADSR.pack(side=LEFT, fill="both", expand="yes", )
        self.attackS = Slider(frameADSR,'attack',
                           ini=0.01,from_=0.0,to=0.5,step=0.005,orient=HORIZONTAL,packSide=TOP) 

        self.decayS = Slider(frameADSR,'decay',
                           ini=0.01,from_=0.0,to=0.5,step=0.005,orient=HORIZONTAL,packSide=TOP)

        self.sustainS = Slider(frameADSR,'sustain',
                   ini=0.4,from_=0.0,to=1.0,step=0.01,orient=HORIZONTAL,packSide=TOP) 
                    
        self.releaseS = Slider(frameADSR,'release',
                   ini=0.5,from_=0.0,to=4.0,step=0.05,orient=HORIZONTAL,packSide=TOP) 
        
        # canales indexados por la nota de lanzamiento -> solo una nota del mismo valor
        self.channels = dict()        
        self.tails = dict()

    def set_waveform(self, shape):
        self.shape = shape
        print(f"Forma de onda cambiada a: {shape}")

    def set_waveformM(self, shape):
        self.shapeM = shape
        print(f"Forma de onda moduladora cambiada a: {shape}")                    

    # obtenemos todos los parámetros del sinte (puede servir para crear presets)
    def getConfig(self):
        return (self.ampS.get(),self.ratioS.get(),self.betaS.get(),
                self.attackS.get(), self.decayS.get(), self.sustainS.get(),
                self.releaseS.get())

    # activación de nota
    def noteOn(self,midiNote):
        # si está el dict de canales apagamos nota actual con envolvente de fadeout
        # y guardamos en tails. El next devolverá este tail y luego comenzará la nota
        if midiNote in self.channels:                   
            lastAmp = self.channels[midiNote].adsr.last # ultimo valor de la envolvente: inicio del fadeOut
            env = Env([(0,lastAmp),(CHUNK,0)]).next()   # envolvente             
            signal = self.channels[midiNote].next()     # señal          
            self.tails[midiNote] = env*signal           # diccionario de tails (notas apagadas) 

        # generamos un nuevo synth en un canal indexado con notaMidi
        # con los parámetros actuales del synth
        freq= freqsMidi[midiNote]
        self.channels[midiNote]= SynthFM(
                fc=freq,
                amp=self.ampS.get(), ratio=self.ratioS.get(), beta=self.betaS.get(),
                attack = self.attackS.get(), decay= self.decayS.get(),
                sustain=self.sustainS.get(), release=self.releaseS.get(), shape = self.shape, shapeM = self.shapeM)

    # apagar nota -> propagamos noteOff al synth, que se encargará de hacer el release
    def noteOff(self,midiNote):
        if midiNote in self.channels: # está el dict, release
            self.channels[midiNote].noteOff()


    # lectura de teclas de teclado como eventos tkinter
    def down(self,event):
        c = event.keysym

        # tecla "panic" -> apagamos todos los sintes de golpe!
        if c=='0': 
            self.stop()            
        elif c in teclas:
            midiNote = 48+teclas.index(c) # buscamos indice y trasnportamos a C3 (48 en midi)        
            print(f'noteOn {midiNote}')
            self.noteOn(midiNote)         # arrancamos noteOn con el instrumento 
            

    def up(self,event):
        c = event.keysym
        if c in teclas:
            midiNote = 48+teclas.index(c) # buscamos indice y hacemos el noteOff
            print(f'noteOff {midiNote}')
            self.noteOff(midiNote)

    # siguiente chunck del generador: sumamos señal de canales y hacemos limpia de silenciados
    def next(self):
        out = np.zeros(CHUNK)          
        for c in list(self.channels):            # convertimos las keys a lista para mantener la lista de claves original
            if self.channels[c].state == 'off':  # si no, modificamos diccionario en el bucle de recorrido de claves -> error 
                del self.channels[c]
            else: # si la nota está el diccionario de tails devolvemos el fadeout generado en noteOn y elminamos tail
                if c in self.tails:                  
                    out += self.tails[c]
                    del self.tails[c]
                else:
                    out += self.channels[c].next()
        return out        

    # boton del pánico
    def stop(self):
        self.channels = dict() # delegamos en el garbage collector
        # for c in list(self.channels): del self.channels[c]

#%%
# Prueba ejercicio 1

from tkinter import *
import os
#from instrument import *
import sounddevice as sd


def test():
    def callback(outdata, frames, time, status):    
        if status: print(status)    
        s = np.sum([i.next() for i in inputs],axis=0)
        s = np.float32(s)
        outdata[:] = s.reshape(-1, 1)

    tk = Tk()
    ins = InstrumentNew1(tk)
    inputs = [ins]

    # desactivar repeticion de teclas
    os.system('xset r off')

    stream = sd.OutputStream(samplerate=SRATE, channels=1, blocksize=CHUNK, callback=callback)    
    stream.start()
    tk.mainloop()

    # reactivar repeticion de teclas   
    os.system('xset r on')
    stream.close()

test()    


#%%
# EJERCICIO 4 EVALUABLE : Modificar la clase Instrumento para poder controlar dos instrumentos simultáneamente.
# El primero vendrá controlado por las 2 las inferiores del teclado zsxdcvgbhnjm y el segundo por las dos superiores q2w3er5t6y7u

# La clase original Instrumento tiene mapeado zsxdcvgbhnjmq2w3er5t6y7u, por lo que tiene acceso a 2 octavas, sin embargo, no 
# podría tocar 2 veces la misma nota a la vez. En este ej, la idea es reducir a 1 octava, pero teniendo 2 pianos

# Basicamente se duplica todo respecto a la clase Instrument, todos los sliders, los canales y las funciones que trabajan sobre
# el mapeo anterior.

# Instrument crea una interfaz TKInter que muestra los sliders y el cuadro de texto, a este cuadro de texto se le activan los eventos
# de presion de tecla, cuando se presiona una tecla, se activa la funcion down, que se encarga de comprobar el mapeo, calcular el midi
# y llamar a la funcion noteOn, lo mismo cuando se deja de presionar una tecla, se llama a la funcion noteOff.
# Cada instrumento tiene un canal para cada nota, y un diccionario de tails, que guarda las notas que se han dejado de presionar
# La funcion noteOn comprueba si la nota ya está en el canal, si está, se guarda en tails, si no, se crea un nuevo canal con un synthFM
# La funcion noteOff comprueba si la nota está en el canal, para apagarla (llamar a noteOff del synthFM)

# El callback crea un hilo distinto con un flujo de audio sin necesidad de un flujo explicito, este hilo se matará al cerrar la ventana

import numpy as np   
import matplotlib.pyplot as plt
from consts import *
from tkinter import *
from slider import *
from adsr import *
from synthFM import *

teclas= "zsxdcvgbhnjm"
teclas2 = "q2w3er5t6y7u"  # 2 de teclas filas 

class InstrumentNew:
    def __init__(self,tk,name="FM synthetizer",amp=0.2,ratio=3,beta=0.6): 
        
        frame = LabelFrame(tk, text=name, bg="#808090")
        frame.pack(side=LEFT)
        # Synth params con sus sliders
        frameOsc = LabelFrame(frame, text="FM oscillator", bg="#808090")
        frameOsc.pack(side=LEFT, fill="both", expand="yes")
        
        self.ampS = Slider(frameOsc,'amp',packSide=TOP,
                           ini=amp,from_=0.0,to=1.0,step=0.05) 

        self.ratioS = Slider(frameOsc,'ratio',packSide=TOP,
                           ini=ratio,from_=0.0,to=20.0,step=0.5)
    
        self.betaS = Slider(frameOsc,'beta',packSide=TOP,
                            ini=beta,from_=0.0,to=10.0,step=0.05) 
        
        # una ventana de texto interactiva para poder lanzar notas con el teclado del ordenador
        text = Text(frameOsc,height=4,width=40)
        text.pack(side=BOTTOM)
        text.bind('<KeyPress>', self.down)
        text.bind('<KeyRelease>', self.up)

       
        # ADSR params con sus sliders
        frameADSR = LabelFrame(frame, text="ADSR", bg="#808090")
        frameADSR.pack(side=LEFT, fill="both", expand="yes", )
        self.attackS = Slider(frameADSR,'attack',
                           ini=0.01,from_=0.0,to=0.5,step=0.005,orient=HORIZONTAL,packSide=TOP) 

        self.decayS = Slider(frameADSR,'decay',
                           ini=0.01,from_=0.0,to=0.5,step=0.005,orient=HORIZONTAL,packSide=TOP)

        self.sustainS = Slider(frameADSR,'sustain',
                   ini=0.4,from_=0.0,to=1.0,step=0.01,orient=HORIZONTAL,packSide=TOP) 
                    
        self.releaseS = Slider(frameADSR,'release',
                   ini=0.5,from_=0.0,to=4.0,step=0.05,orient=HORIZONTAL,packSide=TOP) 


        
        # canales indexados por la nota de lanzamiento -> solo una nota del mismo valor
        self.channels = dict()        
        self.tails = dict()


        # Synth params con sus sliders
        frameOsc2 = LabelFrame(frame, text="FM oscillator", bg="#808090")
        frameOsc2.pack(side=LEFT, fill="both", expand="yes")
        
        self.ampS2 = Slider(frameOsc2,'amp',packSide=TOP,
                           ini=amp,from_=0.0,to=1.0,step=0.05) 

        self.ratioS2 = Slider(frameOsc2,'ratio',packSide=TOP,
                           ini=ratio,from_=0.0,to=20.0,step=0.5)
    
        self.betaS2 = Slider(frameOsc2,'beta',packSide=TOP,
                            ini=beta,from_=0.0,to=10.0,step=0.05) 

       
        # ADSR params con sus sliders
        frameADSR2 = LabelFrame(frame, text="ADSR", bg="#808090")
        frameADSR2.pack(side=LEFT, fill="both", expand="yes", )
        self.attackS2 = Slider(frameADSR2,'attack',
                           ini=0.01,from_=0.0,to=0.5,step=0.005,orient=HORIZONTAL,packSide=TOP) 

        self.decayS2 = Slider(frameADSR2,'decay',
                           ini=0.01,from_=0.0,to=0.5,step=0.005,orient=HORIZONTAL,packSide=TOP)

        self.sustainS2 = Slider(frameADSR2,'sustain',
                   ini=0.4,from_=0.0,to=1.0,step=0.01,orient=HORIZONTAL,packSide=TOP) 
                    
        self.releaseS2 = Slider(frameADSR2,'release',
                   ini=0.5,from_=0.0,to=4.0,step=0.05,orient=HORIZONTAL,packSide=TOP) 
        
        self.channels2 = dict()        
        self.tails2 = dict()
                         

    # obtenemos todos los parámetros del sinte (puede servir para crear presets)
    def getConfig(self):
        return (self.ampS.get(),self.ratioS.get(),self.betaS.get(),
                self.attackS.get(), self.decayS.get(), self.sustainS.get(),
                self.releaseS.get())

    # activación de nota
    def noteOn1(self,midiNote):
        # si está el dict de canales apagamos nota actual con envolvente de fadeout
        # y guardamos en tails. El next devolverá este tail y luego comenzará la nota
        if midiNote in self.channels:                   
            lastAmp = self.channels[midiNote].adsr.last # ultimo valor de la envolvente: inicio del fadeOut
            env = Env([(0,lastAmp),(CHUNK,0)]).next()   # envolvente             
            signal = self.channels[midiNote].next()     # señal          
            self.tails[midiNote] = env*signal           # diccionario de tails (notas apagadas) 

        # generamos un nuevo synth en un canal indexado con notaMidi
        # con los parámetros actuales del synth
        freq= freqsMidi[midiNote]
        self.channels[midiNote]= SynthFM(
                fc=freq,
                amp=self.ampS.get(), ratio=self.ratioS.get(), beta=self.betaS.get(),
                attack = self.attackS.get(), decay= self.decayS.get(),
                sustain=self.sustainS.get(), release=self.releaseS.get())
        
    def noteOn2(self,midiNote):
        # si está el dict de canales apagamos nota actual con envolvente de fadeout
        # y guardamos en tails. El next devolverá este tail y luego comenzará la nota
        if midiNote in self.channels2:                   
            lastAmp = self.channels2[midiNote].adsr.last # ultimo valor de la envolvente: inicio del fadeOut
            env = Env([(0,lastAmp),(CHUNK,0)]).next()   # envolvente             
            signal = self.channels2[midiNote].next()     # señal          
            self.tails2[midiNote] = env*signal           # diccionario de tails (notas apagadas) 

        # generamos un nuevo synth en un canal indexado con notaMidi
        # con los parámetros actuales del synth
        freq= freqsMidi[midiNote]
        self.channels[midiNote]= SynthFM(
                fc=freq,
                amp=self.ampS.get(), ratio=self.ratioS.get(), beta=self.betaS.get(),
                attack = self.attackS.get(), decay= self.decayS.get(),
                sustain=self.sustainS.get(), release=self.releaseS.get())

    # apagar nota -> propagamos noteOff al synth, que se encargará de hacer el release
    def noteOff1(self,midiNote):
        if midiNote in self.channels: # está el dict, release
            self.channels[midiNote].noteOff()
    # apagar nota -> propagamos noteOff al synth, que se encargará de hacer el release
    def noteOff2(self,midiNote):
        if midiNote in self.channels: # está el dict, release
            self.channels[midiNote].noteOff()


    # lectura de teclas de teclado como eventos tkinter
    def down(self,event):
        c = event.keysym

        # tecla "panic" -> apagamos todos los sintes de golpe!
        if c=='0': 
            self.stop()            
        elif c in teclas:
            midiNote = 48+teclas.index(c) # buscamos indice y trasnportamos a C3 (48 en midi)        
            print(f'noteOn {midiNote}')
            self.noteOn1(midiNote)
        elif c in teclas2:
            midiNote = 48+teclas2.index(c) # buscamos indice y trasnportamos a C3 (48 en midi)        
            print(f'noteOnEspecial {midiNote}')
            self.noteOn2(midiNote)         # arrancamos noteOn con el instrumento 
            

    def up(self,event):
        c = event.keysym
        if c in teclas:
            midiNote = 48+teclas.index(c) # buscamos indice y hacemos el noteOff
            print(f'noteOff {midiNote}')
            self.noteOff1(midiNote)
        if c in teclas2:
            midiNote = 48+teclas2.index(c) # buscamos indice y hacemos el noteOff
            print(f'noteOff {midiNote}')
            self.noteOff2(midiNote)

    # siguiente chunck del generador: sumamos señal de canales y hacemos limpia de silenciados
    def next(self):
        out = np.zeros(CHUNK)          
        for c in list(self.channels):            # convertimos las keys a lista para mantener la lista de claves original
            if self.channels[c].state == 'off':  # si no, modificamos diccionario en el bucle de recorrido de claves -> error 
                del self.channels[c]
            else: # si la nota está el diccionario de tails devolvemos el fadeout generado en noteOn y elminamos tail
                if c in self.tails:                  
                    out += self.tails[c]
                    del self.tails[c]
                else:
                    out += self.channels[c].next()
        
        for c in list(self.channels2):            # convertimos las keys a lista para mantener la lista de claves original
            if self.channels2[c].state == 'off':  # si no, modificamos diccionario en el bucle de recorrido de claves -> error 
                del self.channels2[c]
            else: # si la nota está el diccionario de tails devolvemos el fadeout generado en noteOn y elminamos tail
                if c in self.tails2:                  
                    out += self.tails2[c]
                    del self.tails2[c]
                else:
                    out += self.channels2[c].next()
        return out        

    # boton del pánico
    def stop(self):
        self.channels = dict() # delegamos en el garbage collector
        # for c in list(self.channels): del self.channels[c]

# %%
# Prueba ejercicio 4

from tkinter import *
import os
#from instrument import *
import sounddevice as sd


def test():
    def callback(outdata, frames, time, status):    
        if status: print(status)    
        s = np.sum([i.next() for i in inputs],axis=0)
        s = np.float32(s)
        outdata[:] = s.reshape(-1, 1)

    tk = Tk()
    ins = InstrumentNew(tk)
    inputs = [ins]

    # desactivar repeticion de teclas
    os.system('xset r off')

    stream = sd.OutputStream(samplerate=SRATE, channels=1, blocksize=CHUNK, callback=callback)    
    stream.start()
    tk.mainloop()

    # reactivar repeticion de teclas   
    os.system('xset r on')
    stream.close()

test()    

# %%
