# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 17:23:38 2018

@author: Agus
"""
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt


class AudioControl:
  
    fs=48000
    ampMax=1
    
    def crearOnda(frec,amp=ampMax,long=1,offset=0):
        t=np.arange(long*fs)
        return amp*np.sin(2*np.pi*frec*t/fs)+offset
    """"Revisar valores de amplitud (máximos y eso). Suponemos que va entre 1 y menos 1
    hay algún tema con escribir las variables adentro y afuera de la clase"""
    
    
    def test():
        sd.play(np.stack((AudioControl.crearOnda(440),AudioControl.crearOnda(440,amp=0)), axis=-1))
        sd.wait()
        sd.play(np.stack((AudioControl.crearOnda(440,amp=0),AudioControl.crearOnda(440)), axis=-1))
        sd.wait()
        print('Tendría que haber escuchado 1 segundo de audio en cada canal')
        
    def crearRect (frec,amp=ampMax,long=1,offset=0):
        t=np.arange(long*fs)
        T_samples=t*frec/fs
        T_samples=T_samples-np.trunc(T_samples)
        return np.where(T_samples<0.5,1,0)*amp+offset
        
    def crearRamp(Vin,Vend):
        pass
        
            