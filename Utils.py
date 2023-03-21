#Utils.py Utiliy functions
from typing import Union
import numpy as np
from datetime import datetime

log = []

def Vector2(x: Union[float,int],y: Union[float,int]):
    # Utility function for more readible Vector2 construction

    return np.array([x,y])

def Normalize(arr: np.ndarray, tMin: Union[float,int]=-1, tMax: Union[float,int]=1):
    #Util function for normalizing vectors

    normArr = np.zeros(arr.size)
    diff = tMax - tMin
    diffArr = max(arr) - min(arr)   
    i = 0
    for v in arr:
        temp = (((v - min(arr))*diff)/diffArr) + tMin
        normArr[i] = temp
        i+=1
    return normArr.astype(arr.dtype)

def Log(*args: tuple):
    #Log function to allow logging accross different modules
    global log

    t = formatted_time = datetime.now().strftime("%H:%M:%S:%f")[:-3]

    txt = ' '.join(str(arg) for arg in args)
    log.append(f"| {t} | {txt}")

def OutputLog():
    # Function to output latest log messages

    global log
    for txt in log:
        print(txt)
    log.clear()
