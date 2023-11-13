from desarrollo import read_WAV_file
import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sig
import pandas as pd
import librosa

def plot_signal(signal, samplerate, title):
    tiempo = []
    for i in range(len(signal)):
        tiempo.append(i/samplerate)

    plt.plot(signal)
    plt.xlabel("Tiempo [s]")
    plt.ylabel("Amplitud")
    plt.title(title, fontsize=16)
    plt.show()

def plot_transformada(transformada, samplerate, title):
    frecuencia = []
    for i in range(len(transformada)):
        frecuencia.append(i*(samplerate/2)/len(transformada))

    transformada = 10*np.log10(transformada/np.max(transformada))
    transformada = pd.Series(transformada)
    transformada = transformada.rolling(100).mean()

    # plt.plot(frecuencia, transformada)
    # plt.xlabel("Frecuencia [Hz]")
    # plt.ylabel("Amplitud")
    # plt.title(title, fontsize=16)
    # plt.show()

    return transformada


def carac ():
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

    conv = sig.fftconvolve(sweep_data, filtro_data, mode='same')
    plot_signal(conv, sweep_sr, "Convolucion")

def recortar (convolucion):
    idx = np.argmax(convolucion)
    init = idx - 2000
    end = idx + 99000
    return convolucion[init : end]


def rta_impulso ():
    sweep_datam, sweep_srm = read_WAV_file("/Users/serena/Desktop/UDESA/Analisis matematico III/TP2-AIII/mediciones_tp2/respuesta_impulso/con_mochilas/Sweep.wav")
    # plot_signal(sweep_datam, sweep_srm, "Sweep con mochilas")
    sweep_datas, sweep_srs = read_WAV_file("/Users/serena/Desktop/UDESA/Analisis matematico III/TP2-AIII/mediciones_tp2/respuesta_impulso/sin_mochilas/Sweep sin mochilas.wav")
    plot_signal(sweep_datas, sweep_srs, "Sweep sin mochilas")

    filtro_data, filtro_sr = read_WAV_file('/Users/serena/Desktop/UDESA/Analisis matematico III/TP2-AIII/mediciones_tp2/invfilt_udesa_20_20000.wav')

    conv_m = sig.fftconvolve(sweep_datam, filtro_data, mode='full')
    # plot_signal(conv_m, sweep_srm, "Convolucion con mochilas")

    conv_m = recortar(conv_m)
    # plot_signal(conv_m, sweep_srm, "Convolucion con mochilas")

    transformada_m = abs(np.fft.fft(conv_m))
    transformada_m = transformada_m[0:int(len(transformada_m)/2)]
    transformada_m = plot_transformada(transformada_m, sweep_srm, "Transformada de la convolucion con mochilas")

    conv_s = sig.fftconvolve(sweep_datas, filtro_data, mode='same')
    # plot_signal(conv_s, sweep_srs, "Convolucion sin mochilas")

    conv_s = recortar(conv_s)

    transformada_s = abs(np.fft.fft(conv_s))
    transformada_s = transformada_s[0:int(len(transformada_s)/2)]
    transformada_s = plot_transformada(transformada_s, sweep_srs, "Transformada de la convolucion sin mochilas")

    return transformada_m, transformada_s


def resample_to_44100 (amp, sr):
    resample_factor = 44100 / sr
    return librosa.resample(amp, orig_sr=sr, target_sr=44100)

def estandarizar_frecuencia_muestreo(arreglo_amplitud, frecuencia_actual, frecuencia_objetivo=44100):
    amplitud = []
    sr = []

    for i in range(len(arreglo_amplitud)):
        resampled = resample_to_44100(arreglo_amplitud[i], frecuencia_actual[i])

        amplitud.append(resampled)
        sr.append(frecuencia_objetivo)

    return amplitud, sr

def transformadas (amps):
    ffts = []
    for amp in amps:
        fft = abs(np.fft.fft(amp))
        fft = fft[0:int(len(fft)/2)]
        fft = 10*np.log10(fft/np.max(fft))
        fft = pd.Series(fft)
        fft = fft.rolling(100).mean()
        ffts.append(fft)

    return ffts

def comparar (fft_r, fft_s):
    error = []
    nombres = ['Warehouse', 'Typing', 'Summer', 'Snow', 'Tennis', 'Mine', 'Tunnel', 'Nuclear', 'Church', 'Sports', 'Trollers', 'Monument', 'Symphony']

    for i in range(len(fft_r)):
        fft = fft_r[i]

        error.append(np.mean((fft - fft_s)**2))
        
    print(error)
    plt.bar (nombres, error)
    plt.xlabel("Recintos")
    plt.ylabel("Error")
    plt.show()



def recintos ():
    warehouse, warehouse_sr = read_WAV_file('/Users/serena/Desktop/UDESA/Analisis matematico III/TP2-AIII/rirs_recintos/terrys-factory-warehouse/mono/terrys_warehouse_omni.wav')
    typing, typing_sr = read_WAV_file('/Users/serena/Desktop/UDESA/Analisis matematico III/TP2-AIII/rirs_recintos/terrys-typing-room/mono/terrys_typing_omni.wav')
    summer, summer_sr = read_WAV_file('/Users/serena/Desktop/UDESA/Analisis matematico III/TP2-AIII/rirs_recintos/koli-national-park-summer/mono/koli_summer_site1_1way_mono.wav')
    snow, snow_sr = read_WAV_file('/Users/serena/Desktop/UDESA/Analisis matematico III/TP2-AIII/rirs_recintos/koli-national-park-winter/mono/koli_snow_site1_1way_mono.wav')
    tennis, tennis_sr = read_WAV_file('/Users/serena/Desktop/UDESA/Analisis matematico III/TP2-AIII/rirs_recintos/falkland-palace-royal-tennis-court/mono/falkland_tennis_court_omni.wav')
    mine, mine_sr = read_WAV_file('/Users/serena/Desktop/UDESA/Analisis matematico III/TP2-AIII/rirs_recintos/gill-heads-mine/mono/mine_site1_1way_mono.wav')
    tunnel, tunnel_sr = read_WAV_file('/Users/serena/Desktop/UDESA/Analisis matematico III/TP2-AIII/rirs_recintos/innocent-railway-tunnel/mono/tunnel_entrance_a_1way_mono.wav')
    nuclear, nuclear_sr = read_WAV_file('/Users/serena/Desktop/UDESA/Analisis matematico III/TP2-AIII/rirs_recintos/r1-nuclear-reactor-hall/mono/r1_omni_48k.wav')
    church, church_sr = read_WAV_file('/Users/serena/Desktop/UDESA/Analisis matematico III/TP2-AIII/rirs_recintos/shrine-and-parish-church-all-saints-north-street-_/mono/r1.wav')
    sports, sports_sr = read_WAV_file('/Users/serena/Desktop/UDESA/Analisis matematico III/TP2-AIII/rirs_recintos/sports-centre-university-york/mono/sportscentre_omni.wav')
    trollers, trollers_sr = read_WAV_file('/Users/serena/Desktop/UDESA/Analisis matematico III/TP2-AIII/rirs_recintos/trollers-gill/mono/dales_site1_1way_mono.wav')
    monument, monument_sr = read_WAV_file('/Users/serena/Desktop/UDESA/Analisis matematico III/TP2-AIII/rirs_recintos/tyndall-bruce-monument/mono/tyndall_bruce_omni.wav')
    symphony, symphony_sr = read_WAV_file('/Users/serena/Desktop/UDESA/Analisis matematico III/TP2-AIII/rirs_recintos/usina-del-arte-symphony-hall/mono/ir_posic2-pb_-_sfdc.wav')

    recinto = [warehouse, typing, summer, snow, tennis, mine, tunnel, nuclear, church, sports, trollers, monument, symphony]
    sr = [warehouse_sr, typing_sr, summer_sr, snow_sr, tennis_sr, mine_sr, tunnel_sr, nuclear_sr, church_sr, sports_sr, trollers_sr, monument_sr, symphony_sr]
    recinto, sr = estandarizar_frecuencia_muestreo(recinto, sr)


    for res in recinto:

        idx = np.argmax(res)
        if idx > 1000:
            init = idx - 1000
            end = idx + 109000
        else:
            init = 0
            end = 110000
        res = res[init : end]

    ffts = transformadas(recinto)
    
    sweep_mochila, sweep_sin_m = rta_impulso()

    comparar (ffts, sweep_sin_m)


# rta_impulso()

# recintos()