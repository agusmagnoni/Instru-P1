# -*- coding: utf-8 -*-
"""
Created on Mon Aug 27 17:23:38 2018

@author: Agus
"""
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt


class AudioControl(object):
    
    def __init__(self):
        self.fs=48000
        self.ampMax=1
    
    def crearOnda(self, frec,amp=None,long=1,offset=0):
        if amp is None:
            amp=self.ampMax
        t=np.arange(long*self.fs)
        return amp*np.sin(2*np.pi*frec*t/self.fs)+offset
    """"Revisar valores de amplitud (máximos y eso). Suponemos que va entre 1 y menos 1
    hay algún tema con escribir las variables adentro y afuera de la clase"""
    
    
    def test(self):
        sd.play(np.stack((self.crearOnda(440),self.crearOnda(440,amp=0)), axis=-1))
        sd.wait()
        sd.play(np.stack((self.crearOnda(440,amp=0),self.crearOnda(440)), axis=-1))
        sd.wait()
        print('Tendría que haber escuchado 1 segundo de audio en cada canal')
        
    def crearRect (self,frec,amp=None,long=1,offset=0):
        if amp is None:
            amp=self.ampMax
        t=np.arange(long*self.fs)
        T_samples=t*frec/self.fs
        T_samples=T_samples-np.trunc(T_samples)
        return np.where(T_samples<0.5,1,0)*amp+offset
        
    def crearRamp(Vin,Vend):
        pass
        
            