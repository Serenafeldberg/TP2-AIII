import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf

def read_WAV_file (path):

    data, samplerate = sf.read(path)
    print("La maxima amplitud es: ", np.max(data))
    print("La minima amplitud es: ", np.min(data))
    print("La frecuencia de muestreo es: ", samplerate)
    print("La cantidad de muestras es: ", len(data))

    plt.plot(data)
    plt.xlabel("Tiempo (s) / muestras")
    plt.ylabel("Amplitud")
    plt.show()

    return data, samplerate

def plot_fourier (data, samplerate):

    dft = abs(np.fft.fft(data)) 
    frecuencias = abs(np.fft.fftfreq(len(dft), 1.0 / samplerate)) 
    plt.figure(figsize=(10, 4))
    plt.plot(frecuencias, np.abs(dft), color='b')
    plt.title('DFT de la Señal de Audio')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Magnitud')
    plt.grid(True)
    plt.show() 
    return len(frecuencias)

def plot_espectro_de_frec(data, samplerate):
    
    n = len(data)
    k = np.arange(n)
    T = n / samplerate
    frq = k / T
    frq = frq[range(n//2)]
    Y = np.fft.fft(data) / n
    Y = Y[range(n//2)]
    plt.figure(figsize=(10, 4))
    plt.plot(frq, abs(Y), 'r', lw=0.5)
    plt.title('Espectro')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('|Y(freq)|')
    plt.grid(True)
    plt.show()

def plot_filtro_inverso(data, samplerate):  #no se que es esto
  
   




def main():
    data6, samplerate6 = read_WAV_file("/Users/serena/Desktop/UDESA/Analisis matematico III/TP2-AIII/mediciones_tp2/caracterizacion_fuentes/lunes/carac_fuentes_6globos.wav")
    fourier6 = plot_fourier(data6, samplerate6)
    
    


if __name__ == '__main__':
    main()