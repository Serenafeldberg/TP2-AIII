from desarrollo import read_WAV_file
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sig

def plot_signal(signal, samplerate, title):
    tiempo = []
    for i in range(len(signal)):
        tiempo.append(i/samplerate)

    plt.plot(tiempo, signal)
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Amplitud")
    plt.title(title, fontsize=16)
    plt.show()

def plot_transformada(transformada, samplerate, title):
    frecuencia = []
    for i in range(len(transformada)):
        frecuencia.append(i*(samplerate/2)/len(transformada))

    transformada = 10*np.log10(transformada/np.max(transformada))

    plt.plot(frecuencia, transformada)
    plt.xlabel("Frecuencia [Hz]")
    plt.ylabel("Amplitud")
    plt.title(title, fontsize=16)
    plt.show()


sweep_data, sweep_sr = read_WAV_file("/Users/serena/Desktop/UDESA/Analisis matematico III/TP2-AIII/mediciones_tp2/sweep_udesa_20_20000.wav")
# plot_signal(sweep_data, sweep_sr, "Sweep")

transformada_s = abs(np.fft.fft(sweep_data))
transformada_s = transformada_s[0:int(len(transformada_s)/2)]
# plot_transformada(transformada_s, sweep_sr, "Transformada del sweep")


filtro_data, filtro_sr = read_WAV_file('/Users/serena/Desktop/UDESA/Analisis matematico III/TP2-AIII/mediciones_tp2/invfilt_udesa_20_20000.wav')
# plot_signal(filtro_data, filtro_sr, "Filtro")

transformada_f = abs(np.fft.fft(filtro_data))
transformada_f = transformada_f[0:int(len(transformada_f)/2)]
# plot_transformada(transformada_f, filtro_sr, "Transformada del filtro")

conv_f = transformada_s * transformada_f

plot_signal(conv_f, sweep_sr, "Convolucion en frecuencia")

conv = sig.fftconvolve(sweep_data, filtro_data, mode='same')
plot_signal(conv, sweep_sr, "Convolucion")