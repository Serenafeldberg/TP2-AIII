import numpy as np

def mismo (data):
    step = 10000
    for i in range(len(data)):
        index = np.argmax(data[i])
        init = index - step
        end = index + step
        data[i] = data[i][init : end]

    return data

def recorte_aplausos (aplausos):
    data_mochila = aplausos[0][0]
    d_mochila = []

    d_mochila.append(data_mochila[100000:250000])
    d_mochila.append(data_mochila[250000:400000])


    data_sin_mochila = aplausos[1][0]
    d_sin_mochila = []

    d_sin_mochila.append(data_sin_mochila[50000:150000])
    d_sin_mochila.append(data_sin_mochila[150000:250000])
    d_sin_mochila.append(data_sin_mochila[250000:350000])

    return mismo(d_mochila), mismo(d_sin_mochila)

def recorte_globos (globos):
    data_mochila = globos[0][0]
    d_mochila = []

    d_mochila.append(data_mochila[200000:400000])
    d_mochila.append(data_mochila[500000:800000])


    data_sin_mochila = globos[1][0]
    d_sin_mochila = [data_sin_mochila]

    return mismo(d_mochila), mismo(d_sin_mochila)

def recorte_maderas (maderas):
    data_mochila = maderas[0][0]
    d_mochila = []

    d_mochila.append(data_mochila[100000:350000])
    d_mochila.append(data_mochila[350000:600000])


    data_sin_mochila = maderas[1][0]
    d_sin_mochila = []

    d_sin_mochila.append(data_sin_mochila[80000:240000])
    d_sin_mochila.append(data_sin_mochila[240000:400000])

    return mismo(d_mochila), mismo(d_sin_mochila)