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
       
    def calculo_potencia(self,data):
        return np.sum(data[len(data)//3:2*len(data)//3]**2)/(len(data)//3)
    
    def barrido_frecuencia_onda(self,frec_min,frec_max,pasos=15,amp=None,long=10):
        "Genera un vector de frecuencias entre la mínima y la máxima, con los pasos especificados. Manda funcines senoidales de esa frencuencia y graba la respuesta. Devuelve (por ahora) el vector de frecuencias y un gráfico que muestra la amplitud máxima registrada (puede mejorarse como la obtiene) en función de la frecuencia.CALCULAR LÍMITE TEORICO"
        frecs=np.logspace(np.log10(frec_min),np.log10(frec_max),num=pasos)
        output = np.zeros([pasos,5])
        for i in range(len(frecs)):
            frec=frecs[i]
            output[i,0]=frecs[i] # primer dato freec, segundo pot de entrada, tercero y cuarto pot de salida
            rec=sd.playrec(self.crearOnda(frec,amp=amp,long=long),self.fs,channels=2)
            sd.wait()
            channels = [0,1]
            for channel in channels:
                output[i,3+channel]= self.calculo_potencia(rec[:,channel])
                output[i,1+channel]= self.calculo_potencia(self.crearOnda(frec,amp=amp,long=long))
        
        plt.plot(output[:,0],output[:,1],output[:,0],output[:,2],output[:,0],output[:,3],output[:,0],output[:,4],'*')
        return output
    
    def add_cola(self, senal, long=0.2):
        ret=np.concatenate((np.zeros(int(np.round(long*self.fs))),senal,np.zeros(int(np.round(long*self.fs)))))
        return ret
    
    def playrec(self,senal): 
       rec=sd.playrec(senal,self.fs,channels=2)
       sd.wait()
       return rec
   
    def gen_trigger(self,senal):
        t_trig = 0.02
        frec1 = 440
        frec2 = 1000
        samples_triguer = t_trig * self.fs
        N=len(senal)
        if N>samples_triguer * 2:
            c1=self.crearOnda(frec1,long=t_trig)
            c2=np.zeros(int(np.round(N-samples_triguer*2)))
            c3=self.crearOnda(frec2,long=t_trig)
            trig=np.concatenate((c1,c2,c3))
            #plt.figure(1),plt.plot(trig)
            return trig
        else:
            return print('La cantidad de muestras de la señal es insuficiente')
        
    def medicion_sycr(self,senal):
        ###SENAL AUXILIAR####
        rec=self.playrec(np.stack((self.add_cola(self.gen_trigger(senal)),self.add_cola(senal)),axis=-1))
        sd.wait()
        plt.figure(2),plt.plot(rec)
        return rec

        
    
    
    
    
    
    