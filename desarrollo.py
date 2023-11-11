import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf
from scipy.signal import find_peaks

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

def show_recortes (data):
    cant = len(data)
    fig, axs = plt.subplots(cant, figsize=(10, 4))

    for i in range(cant):
        axs[i].plot(data[i])

    plt.show()
        

def mismo_tam (data, step):
    # hacer todos del mismo tamaño --> desde su amplitud maxima, le dejo 100000 muestras
    step = 25000
    for i in range(len(data)):
        index = np.argmax(data[i])
        init = index - step
        end = index + step
        data[i] = data[i][init : end]

    return data

def globos_6 (data, samplerate):
    primero = data[:200000]
    segundo = data[600000:950000]
    tercero = data[950000:1015000]
    cuarto = data[1000000:1200000]
    quinto = data[1200000:1400000]
    sexto = data[1309000:1600000]

    globos = [primero, segundo, tercero, cuarto, quinto, sexto]

    return mismo_tam(globos, 25000)

def aplausos_10 (data):
    aplauso_1 = data[:100000]
    aplauso_2 = data[100000:200000]
    aplauso_3 = data[200000:270000]
    aplauso_4 = data[270000:310000]
    aplauso_5 = data[350000:400000]
    aplauso_6 = data[400000:480000]
    aplauso_7 = data[490000:580000]
    aplauso_8 = data[580000:620000]
    aplauso_9 = data[650000:720000]
    aplauso_10 = data[720000:800000] 
    aplausos = [aplauso_1, aplauso_2, aplauso_3, aplauso_4, aplauso_5, aplauso_6, aplauso_7, aplauso_8, aplauso_9, aplauso_10]

    return mismo_tam(aplausos, 10000)
    # hacer todos del mismo tamaño --> desde su amplitud maxima, le dejo 100000 muestras
    step = 10000
    for i in range(len(aplausos)): 
        index = np.argmax(aplausos[i])
        init = index - step
        end = index + step
        aplausos[i] = aplausos[i][init : end]  
    return aplausos

def maderas_10 (data):
    madera_1 = data[80000:100000]
    madera_2 = data[170000:185000]
    madera_3 = data[250000:270000]
    madera_4 = data[342000:360000]
    madera_5 = data[430000:450000]
    madera_6 = data[520000:540000]
    madera_7 = data[600000:620000]
    madera_8 = data[680000:700000]
    madera_9 = data[780000:800000]
    madera_10 = data[860000:880000]
    maderas= [madera_1, madera_2, madera_3, madera_4, madera_5, madera_6, madera_7, madera_8, madera_9, madera_10]
    
    return mismo_tam(maderas)

def globos_mie (data):
    primero = data[:300000]
    segundo = data[400000:600000]
    tercero = data[700000:900000]
    cuarto = data[900000:1100000]
    quinto = data[1100000:1250000]
    sexto = data[1250000:1500000]
    septimo = data[1600000:1850000]
    octavo = data[1850000:2100000]
    noveno = data[2100000:2300000]
    globos = [primero, segundo, tercero, cuarto, quinto, sexto, septimo, octavo, noveno]

    # return globos

    return mismo_tam(globos, 50000)

def get_medias (impulsos):
    medias = []
    for i in range (len(impulsos[0])):
        data = 0
        for imp in impulsos:
            data += imp[i]
        data = data / len(impulsos)
        medias.append(data)

    return medias

def get_std (impulsos):
    std = []
    for i in range (len(impulsos[0])):
        data = []
        for imp in impulsos:
            data.append(imp[i])
        std.append(np.std(data))

    return std

def std_up_down (means, std):
    up = []
    down = []
    for i in range(len(means)):
        up.append(means[i] + std[i])
        down.append(means[i] - std[i])

    return up, down

def plot_means (means, std, up, down, title):
    # Plot de la media y el desvio estandar
    plt.figure(figsize=(10, 4))
    plt.plot(means, color='b')
    plt.plot(up, color='r')
    plt.plot(down, color='r')
    plt.title(title)
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Amplitud')
    plt.grid(True)
    plt.show()

def transformada (impulsos):
    ts = []
    for i in range(len(impulsos)):
        tsi = (np.fft.fft(impulsos[i]))
        ts.append(abs(tsi[0:1000]))

    return ts

def suavizar (media, up, down, window_size=5):
    # Aplicar un filtro de media móvil a la media
    media_s = np.convolve(media, np.ones(window_size)/window_size, mode='same')

    # Aplicar un filtro de media móvil a la desviación estándar por encima de la media
    up_s = np.convolve(up, np.ones(window_size)/window_size, mode='same')

    # Aplicar un filtro de media móvil a la desviación estándar por debajo de la media
    down_s = np.convolve(down, np.ones(window_size)/window_size, mode='same')

    return media_s, up_s, down_s


def plot_fourier (data, samplerate):
    dft = abs(np.fft.fft(data)) 

    frecuencias = abs(np.fft.fftfreq(len(dft), 1.0 / samplerate)) 
    plt.figure(figsize=(10, 4))
    plt.plot(frecuencias, np.abs(dft), color='b')
    plt.title('DFT de la Señal de Audio')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Magnitud')
    plt.grid(True)
    # plt.show() 
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


# data6, samplerate6 = read_WAV_file("/Users/serena/Desktop/UDESA/Analisis matematico III/TP2-AIII/mediciones_tp2/caracterizacion_fuentes/lunes/carac_fuentes_6globos.wav")
# globos = globos_6(data6, samplerate6)
# medias_globos = get_medias(globos)
# std_globos = get_std(globos)
# up, down = std_up_down(medias_globos, std_globos)
# plot_means(medias_globos, std_globos, up, down, 'Media de los 6 Globos')

# transformada_globos = transformada(globos)
# medias_globost = get_medias(transformada_globos)
# std_globost = get_std(transformada_globos)
# up, down = std_up_down(medias_globost, std_globost)
# plot_means(medias_globost, std_globost, up, down, 'Media de los 6 Globos (Transformada)')

# media_suanizada, up_suanizada, down_suanizada = suavizar(medias_globost, up, down)
# plot_means(media_suanizada, std_globost, up_suanizada, down_suanizada, 'Media de los 6 Globos (Transformada) Suavizada')


data_10a, samplerate_10a = read_WAV_file("/Users/serena/Desktop/UDESA/Analisis matematico III/TP2-AIII/mediciones_tp2/caracterizacion_fuentes/lunes/carac_fuentes_10aplausos.wav")
aplausos = aplausos_10(data_10a)

show_recortes(aplausos)
# medias_aplausos = get_medias(aplausos)
# std_aplausos = get_std(aplausos)
# up, down = std_up_down(medias_aplausos, std_aplausos)
# plot_means(medias_aplausos, std_aplausos, up, down, 'Media de los 10 Aplausos')

# transformada_aplausos = transformada(aplausos)
# medias_aplaust = get_medias(transformada_aplausos)
# std_aplaust = get_std(transformada_aplausos)
# up, down = std_up_down(medias_aplaust, std_aplaust)
# plot_means(medias_aplaust, std_aplaust, up, down, 'Media de los 10 Aplausos (Transformada)')

# media_suanizada, up_suanizada, down_suanizada = suavizar(medias_aplaust, up, down)
# plot_means(media_suanizada, std_aplaust, up_suanizada, down_suanizada, 'Media de los 10 Aplausos (Transformada) Suavizada')


# data_10m, samplerate_10m = read_WAV_file("/Users/serena/Desktop/UDESA/Analisis matematico III/TP2-AIII/mediciones_tp2/caracterizacion_fuentes/lunes/carac_fuentes_10maderas.wav")
# maderas = maderas_10(data_10m)
# medias_maderas = get_medias(maderas)
# std_maderas = get_std(maderas)
# up, down = std_up_down(medias_maderas, std_maderas)
# plot_means(medias_maderas, std_maderas, up, down, 'Media de los 10 Maderas')

# transformada_maderas = transformada(maderas)
# medias_maderast = get_medias(transformada_maderas)
# std_maderast = get_std(transformada_maderas)
# up, down = std_up_down(medias_maderast, std_maderast)
# plot_means(medias_maderast, std_maderast, up, down, 'Media de los 10 Maderas (Transformada)')

# media_suanizada, up_suanizada, down_suanizada = suavizar(medias_maderast, up, down)
# plot_means(media_suanizada, std_maderast, up_suanizada, down_suanizada, 'Media de los 10 Maderas (Transformada) Suavizada')

# data_globos, samplerate_globos = read_WAV_file("/Users/serena/Desktop/UDESA/Analisis matematico III/TP2-AIII/mediciones_tp2/caracterizacion_fuentes/miercoles/Globos.wav")
# globos_m = globos_mie(data_globos)

# show_recortes(globos_m)

