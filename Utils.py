#Utils.py Utiliy functions
import numpy as np

def Vector2(x,y):
    return np.array([x,y])

def Normalize(arr, t_min=-1, t_max=1):
    norm_arr = np.zeros(arr.size)
    diff = t_max - t_min
    diff_arr = max(arr) - min(arr)   
    i = 0
    for v in arr:
        temp = (((v - min(arr))*diff)/diff_arr) + t_min
        norm_arr[i] = temp
        i+=1
    return norm_arr.astype(arr.dtype)