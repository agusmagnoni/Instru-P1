# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 16:13:06 2018
@author: Agus
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 17:23:38 2018
@author: Agus
"""
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy import signal


class AudioControl(object):
    
    def __init__(self):
        self.fs=48000
        self.ampMax=1
    
    def crearOnda(self, frec,amp=None,long=1):
        if amp is None:
            amp=self.ampMax
        t=np.arange(long*self.fs)
        return amp*np.sin(2*np.pi*frec*t/self.fs)
        
    def test(self):
        sd.play(np.stack((self.crearOnda(440),self.crearOnda(440,amp=0)), axis=-1))
        sd.wait()
        sd.play(np.stack((self.crearOnda(440,amp=0),self.crearOnda(440)), axis=-1))
        sd.wait()
        print('Tendría que haber escuchado 1 segundo de audio en cada canal')
        
    def crearRect (self,frec,amp=None,long=10,offset=0):
        '''NO FUNCIONA Y NO SÉ PORQUÉ'''
        if amp is None:
            amp=self.ampMax
        t=np.arange(long*self.fs)
        T_samples=t*frec/self.fs
        T_samples=T_samples-np.trunc(T_samples)
        return np.where(T_samples<0.5,1,0)*amp+offset
        
    def crearRamp(self,Vin,Vend,long=1):
        '''CREO sirve para nada, SACAR SI CONFIRMO ESTO'''
        t=np.arange(long*self.fs)
        return (Vend-Vin)*t/(long*self.fs)+Vin
        
    def crearCons(self,value,long=10):
        '''El parlante  no está hecho para generar una constante.'''
        return print('El parlante no está preparado para emitir una constante.')

    def serrucho(self,Vin,Vend,long=1/440,n=440):
        # así como está, serrucho de 1 seg, a 440 Hz.
        t=np.arange(long*self.fs)
        ret=(Vend-Vin)*t/(long*self.fs)+Vin
        aux=(Vend-Vin)*t/(long*self.fs)+Vin
        for i in range(n):
            ret=np.concatenate([ret,aux])
        return ret
    
    def sawtooth(self, function, frec, amp=0.5,long=1):
        t=np.linspace(0,long,num=self.fs*long)
        if function=='rampa':
            ret=signal.sawtooth(2*np.pi*frec*t)*amp
            return ret 
        if function=='triangular':
            ret=signal.sawtooth(2*np.pi*frec*t,0.5)*amp
            return ret   
        
    def square(self,frec,amp=0.5,long=1):
        t=np.linspace(0,long,num=self.fs*long)
        ret=signal.square(2 * np.pi * frec * t)*amp
        return ret

    def playrec_onda(self, frec,amp=None,long=10):
        "pone una función onda y la graba al mismo tiempo. La salida de esta función es: un gráfico que muestra la señal que mandó y la que midió y el array correspondiente a la medición. "
        myrec=sd.playrec(self.crearOnda(frec,amp=amp,long=long),self.fs,channels=2)
        sd.wait()
        plt.plot(myrec)
        return myrec
                    
    def playrec_sw(self,function,frec,amp=0.5,long=1):
        "pone una función serrucho o triangular y la graba al mismo tiempo. La salida de esta función es: un gráfico que muestra la señal que mandó y la que midió y el array correspondiente a la medición. "
        a=self.sawtooth(function,frec,amp=amp,long=long)
        myrec=sd.playrec(a,self.fs,channels=2)
        sd.wait()
        plt.plot(myrec)#,plt.plot(self.serrucho(Vin,Vend,long=long,n=n))
        return myrec

    def playrec_square(self,frec,amp=0.5,long=1):
        a=self.square(frec,amp=amp,long=long)
        myrec=sd.playrec(a,self.fs,channels=2)
        sd.wait()
        plt.plot(myrec)
        return myrec
    
    def slew_rate(self,frec,amp=0.5,long=1):
        ret=self.playrec_square(frec,amp=amp,long=long)
        sd.wait()
        '''TERMINAR'''
        return 
        
    def barrido_frecuencia(self,frec_min,frec_max,pasos=15,amp=None,long=10):
        "Genera un vector de frecuencias entre la mínima y la máxima, con los pasos especificados. Manda funcines senoidales de esa frencuencia y graba la respuesta. Devuelve (por ahora) el vector de frecuencias y un gráfico que muestra la amplitud máxima registrada (puede mejorarse como la obtiene) en función de la frecuencia.MEJORAR"
        frec=np.linspace(frec_min,frec_max,num=pasos)
        maximos=np.zeros(pasos)
        for i in range(pasos):
            rec=sd.playrec(self.crearOnda(frec[i],amp=amp,long=long),self.fs,channels=2)
            sd.wait()
            maximos[i]=np.max(rec)
        plt.plot(frec,maximos,'.')
        return frec 
   
    
    
    
    
    
    
    