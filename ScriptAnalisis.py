import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from scipy import signal
from datetime import datetime


def ListaTotal(dirFolder):
    listFileRAW = os.listdir(dirFolder)
    listFile = []
    for item in listFileRAW:
        if item.find("OpenHardwareMonitorLog") != -1:
            date_time_obj = datetime.strptime(item[23:33], '%Y-%m-%d')
            listFile.append(date_time_obj)

    listFile = sorted(listFile)

    for i in range(len(listFile)):
        listFile[i] = listFile[i].strftime('%Y-%m-%d')

    return listFile

def Analitic(FileDirect, hora):
    fileRAW = FileDirect

    archivoRAW = pd.read_csv(fileRAW, low_memory=False) 
    archivoRAW = archivoRAW.drop(0)
    archivoRAW["Unnamed: 0"] = pd.to_datetime(archivoRAW["Unnamed: 0"], format="%m/%d/%Y %H:%M:%S")

    archivoRAW = archivoRAW.rename(columns={'Unnamed: 0': 'Time','/amdcpu/0/temperature/0': 'CPU Temp','/atigpu/0/temperature/0': 'GPU Temp','/atigpu/0/load/0': 'GPU Load','/amdcpu/0/load/0': 'CPU Load'})
    
    try:
        archivoHorasSelect = archivoRAW['Time'].dt.hour.to_numpy()
        archivoHorasSelect = np.where(archivoHorasSelect == int(hora))

        lim1 = np.min(archivoHorasSelect)
        lim2 = np.max(archivoHorasSelect)
    except:
        lim1 = 0
        lim2 = np.shape(archivoRAW['Time'].to_numpy())[0]
    

    def parce(columna,DataFrame,limitInf,limitSup,aFloat):
        val = DataFrame[columna][limitInf:limitSup].to_numpy()
        val = np.delete(val,0)

        if aFloat:
            val = val.astype(np.float64)
            val = np.round_(val, decimals = 2) 
        return val

    T = parce("Time",archivoRAW,lim1,lim2,False)
    CT = parce("CPU Temp",archivoRAW,lim1,lim2,True)
    CL = parce("CPU Load",archivoRAW,lim1,lim2,True)
    GT = parce("GPU Temp",archivoRAW,lim1,lim2,True)
    GL = parce("GPU Load",archivoRAW,lim1,lim2,True)

    fig, ax = plt.subplots(figsize=(50, 30))


    fs = 500  # Sampling frequency
    fc = 10  # Cut-off frequency of the filter #Tocar Esto si algo falla o no se ve como quiero + alto mas frecuencia + picos #base 1
    w = fc / (fs / 2) # Normalize the frequency
    b, a = signal.butter(5, w, 'low')

    output = signal.filtfilt(b, a, CT)


    #output = np.delete(output, np.where(output < 0))
    output = np.where(output < 0, 0, output)

    ax.plot(T, output, color='b', label='CPU Temp')
    output = signal.filtfilt(b, a, CL)
    output = np.where(output < 0, 0, output)
    ax.plot(T, output, color='g', label='CPU Load')
    output = signal.filtfilt(b, a, GT)
    output = np.where(output < 0, 0, output)
    ax.plot(T, output, color='r', label='GPU Temp')
    output = signal.filtfilt(b, a, GL)
    output = np.where(output < 0, 0, output)
    ax.plot(T, output, color='k', label='GPU Load')


    xStep = int(lim2 / 35)

    plt.xlabel("Time", fontsize=30)
    plt.ylabel("Load/Temp", fontsize=30)
    plt.yticks(np.arange(0, 105, step=5), fontsize=30)

    plt.xticks(fontsize=30, rotation = 45)#T[np.arange(lim1, lim2-1, step=xStep)],
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))

    plt.legend(loc = 'upper left', fontsize = 30)
    plt.ylim([0, 105])
    plt.grid()
    plt.ioff()
    plt.savefig("Graph.svg", bbox_inches = 'tight')
    #plt.show()
    return None
#Analitic("OpenHardwareMonitorLog-2021-11-15.csv", 16)
