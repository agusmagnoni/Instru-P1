'''
Este archivo contiene las funciones desarrolladas para usar las entradas y salidad de audio y con ellas realizar mediciones experimentales de respuestas de circuitos.
'''


# Importamos paquetes
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy import signal

# Definimos constantes
fs = 48000
ampMax = 0.5 # En valores arbitrarios float que es lo que recibe el paquetes sounddevice
long_d = 3 # En segundos
DEBUG = False


# Definimos funciones utiles

def testOutput():
    sd.play(np.stack((Onda(440),Onda(440,amp=0)), axis=-1))
    sd.wait()
    sd.play(np.stack((Onda(440,amp=0),Onda(440)), axis=-1))
    sd.wait()
    print('Tendría que haber escuchado 1 segundo de audio en cada canal')
    
def slewrate ():
    print ('Falta implementar')
    # Hay que desarrollar esta funcion
    
def calculo_potencia(data,excluir=0.5):
    # Data tiene que ser un array de dimension 1
    if DEBUG:
        print ('Largo original: ' + str(len(data)))
        plt.plot(data,label='Original')
    data_recortada = np.array(data[int(len(data)*excluir/2):int(len(data)-len(data)*excluir/2)])
    if DEBUG:
        print ('Largo recortado: ' + str(len(data_recortada)))
        plt.plot(data_recortada,label='recortada')
        plt.legend()
    return np.sum(data_recortada**2)/(len(data_recortada))


# Definimos funciones de usuario

def playrec_onda(frec,amp=ampMax,long=long_d):
    # pone una función onda y la graba al mismo tiempo. La salida de esta función es: un gráfico que muestra la señal que mandó y la que midió y el array correspondiente a la medición.
    myrec=sd.playrec(Onda(frec,amp=amp,long=long),fs,channels=2)
    sd.wait()
    plt.plot(myrec)
    return myrec

def playrec (data,show=False):
    myrec=sd.playrec(data,fs,channels=2)
    sd.wait()
    if show:
        plt.figure()
        plt.plot(data, label = 'Input')
        plt.plot([data[0] for data in myrec], label = 'Ch1')
        plt.plot([data[1] for data in myrec], label = 'Ch2')
        plt.legend()
    return myrec

def rampa(frec, amp=ampMax, long=long_d):
    t = np.linspace(0,long,num=fs*long)
    return signal.sawtooth(2*np.pi*frec*t)*amp

def triangular(frec, amp=ampMax, long=long_d):
    t = np.linspace(0,long,num=fs*long)
    return signal.sawtooth(2*np.pi*frec*t,0.5)*amp

def square(frec, amp=ampMax, long=long_d):
    t = np.linspace(0,long,num=fs*long)
    return signal.square(2*np.pi*frec*t)*amp

def Onda(frec,amp=ampMax,long=long_d):
    t=np.arange(long*fs)
    return amp*np.sin(2*np.pi*frec*t/fs)

def barrido_frecuencia_sin(frec_min=10,frec_max=1000000,pasos=1000,amp=ampMax,long=long_d):
        "Genera un vector de frecuencias entre la mínima y la máxima, con los pasos especificados. Manda funcines senoidales de esa frencuencia y graba la respuesta. Devuelve (por ahora) el vector de frecuencias y un gráfico que muestra la amplitud máxima registrada (puede mejorarse como la obtiene) en función de la frecuencia.CALCULAR LÍMITE TEORICO"
        if DEBUG:
            print ('Iniciando barrido en frecuencias')
        frecs=np.logspace(np.log10(frec_min),np.log10(frec_max),num=pasos)
        if DEBUG:
            print ('frecuencias a testear')
            print (frecs)
        pot_in_ch1 = []
        pot_in_ch2 = []
        pot_out_ch1 = []
        pot_out_ch2 = []
        for frec in frecs:
            if DEBUG:
                print (frec)
            signal = Onda(frec)
            rec = playrec(signal)
            sd.wait()
            pot_in_ch1 += [calculo_potencia(signal)]
            pot_in_ch2 += [calculo_potencia(signal)]
            pot_out_ch1 += [calculo_potencia(rec[:,0])]
            pot_out_ch2 += [calculo_potencia(rec[:,1])]
            print ('Evaluando frecuencia: ' + str(frec)) # Mejorar esta linea
            
        plt.plot(frecs,pot_in_ch1,label='In_Ch1')
        plt.plot(frecs,pot_in_ch2,label='In_Ch2')
        plt.plot(frecs,pot_out_ch1,label='Out_Ch1')
        plt.plot(frecs,pot_out_ch2,label='Out_ch2')
        plt.legend()
        return frecs, [pot_in_ch1,pot_in_ch2],[pot_out_ch1,pot_out_ch2]
    
def add_cola(signal, long=0.2):
    ret=np.concatenate((np.zeros(int(np.round(long*fs))),signal,np.zeros(int(np.round(long*fs)))))
    return ret

def gen_trigger(senal):
    t_trig = 0.02 # Tiempo que dura la senal de trigger
    frec1 = 440 # Frecuencia del trigger inicial
    frec2 = 1000 # Frecuencia del trigger final
    samples_triguer = t_trig * fs
    N=len(senal)
    if N>samples_triguer * 10: # Pedimos que haya una senal lo suficientemente larga
        c1=Onda(frec1,long=t_trig)
        c2=np.zeros(int(np.round((N-samples_triguer*2)/3)))
        c3=Onda(frec2,long=t_trig)
        c4=np.zeros(int(np.round(2*(N-samples_triguer*2)/3)))
        trig=np.concatenate((c1,c2,c3,c4))
        return trig
    else:
        return print('La cantidad de muestras de la señal no cumple el criterio de ser 10 veces mayor al tamaño de los triggers')
    
def sync(signal):
    print ('Funcion en desar(rollo')
    print ('Esta funcion asume que el Ch1 conecta directamente la salida de audio con la entrada de microfono, y que el Ch2 conecta la salida de audio con la entrada del dispositivo a caracterizar, cuya respuesta llega al Ch2 del microfono.')
    #rec=playrec(np.stack((add_cola(gen_trigger(signal)),add_cola(signal)),axis=-1))
    rec=playrec(np.stack((add_cola(signal),add_cola(gen_trigger(signal))),axis=-1))
    sd.wait()
    plt.figure(2),plt.plot(rec)
    plt.figure(3),plt.plot(add_cola(gen_trigger(signal))),plt.plot(add_cola(signal))
    trig=add_cola(gen_trigger(signal))
    inp=add_cola(signal)
    return rec, inp, trig

def sync_conv(signal):
    print ('Funcion en desarrollo')
    print ('Esta funcion asume que el Ch1 conecta directamente la salida de audio con la entrada de microfono, y que el Ch2 conecta la salida de audio con la entrada del dispositivo a caracterizar, cuya respuesta llega al Ch2 del microfono.')
    rec=playrec(np.stack((add_cola(gen_trigger(signal)),add_cola(signal)),axis=-1))
    sd.wait()
    conv=np.convolve(add_cola(gen_trigger(signal))/np.max(add_cola(gen_trigger(signal))),rec[:,0]/np.max(rec[:,0]),mode='full')
    plt.figure(2),plt.plot(rec)
    plt.figure(3),plt.plot(add_cola(gen_trigger(signal))/np.max(add_cola(gen_trigger(signal)))),plt.plot(rec[:,0]/np.max(rec[:,0]))
    plt.figure(4),plt.plot(conv)
    return rec






















