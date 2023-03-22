#Utils.py Utiliy functions
from __future__ import annotations
import typing
from typing import Union
import numpy as np
from datetime import datetime


class Vector2:
    """Vector2 class"""
    x: float
    y: float
    
    def __init__(self, x: float, y: float) -> Vector2:
        self.x = x
        self.y = y

    @classmethod
    def from_array(cls, array: Union[np.ndarray,tuple[float,float]]) -> Vector2:
        return cls(array[0],array[1])
        
    def __array__(self) -> np.ndarray:
        return np.array([self.x, self.y])
    
    def __iadd__(self, other: Union[Vector2,np.ndarray,float]) -> Vector2:
        if type(other) is Vector2 or type(other) is np.ndarray:
            self.x += other[0]
            self.y += other[1] 
        else:
            self.x += other
            self.y += other
        return self
    
    def __isub__(self, other: Union[Vector2,np.ndarray,float]) -> Vector2:
        if type(other) is Vector2 or type(other) is np.ndarray:
            self.x -= other[0]
            self.y -= other[1] 
        else:
            self.x -= other
            self.y -= other
        return self
    
    def __imul__(self, scalar: Union[Vector2,np.ndarray,float]) -> Vector2:
        if type(scalar) is Vector2 or type(scalar) is np.ndarray:
            self.x *= scalar[0]
            self.y *= scalar[1] 
        else:
            self.x *= scalar
            self.y *= scalar
        return self
    
    def __itruediv__(self, scalar: Union[Vector2,np.ndarray,float]) -> Vector2:
        if type(scalar) is Vector2 or type(scalar) is np.ndarray:
            self.x /= scalar[0]
            self.y /= scalar[1] 
        else:
            self.x /= scalar
            self.y /= scalar
        return self
    
    def __add__(self, other: Union[Vector2,np.ndarray,float]) -> Vector2:
        if type(other) is Vector2 or type(other) is np.ndarray:
            return Vector2(self.x + other[0], self.y + other[1])
        else:
            return Vector2(self.x + other, self.y + other)
    
    def __sub__(self, other: Union[Vector2,np.ndarray,float]) -> Vector2:
        if type(other) is Vector2 or type(other) is np.ndarray:
            return Vector2(self.x - other[0], self.y - other[1])
        else:
            return Vector2(self.x - other, self.y - other)
    
    def __mul__(self, scalar: Union[Vector2,np.ndarray,float]) -> Vector2:
        if type(scalar) is Vector2 or type(scalar) is np.ndarray:
            return Vector2(self.x * scalar[0], self.y * scalar[1])
        else:
            return Vector2(self.x * scalar, self.y * scalar)
    
    def __truediv__(self, scalar: Union[Vector2,np.ndarray,float]) -> Vector2:
        if type(scalar) is Vector2 or type(scalar) is np.ndarray:
            return Vector2(self.x / scalar[0], self.y / scalar[1])
        else:
            return Vector2(self.x / scalar, self.y / scalar)
    
    def __neg__(self) -> Vector2:
        return Vector2(-self.x, -self.y)
    
    def __eq__(self, other: Vector2) -> bool:
        return self.x == other[0] and self.y == other[1]
    
    def __ne__(self, other: Vector2) -> bool:
        return not self.__eq__(other)
    
    def __repr__(self) -> str:
        return f"Vector2({self.x}, {self.y})"
    
    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def __getitem__(self,key: int) -> float:
        if key==0:
            return self.x
        elif key == 1:
            return self.y
    
    def dot(self, other: Vector2) -> float:
        return self.x * other[0] + self.y * other[1]
    
    def length(self) -> float:
        return np.sqrt(self.x**2 + self.y**2)
    
    def normalized(self) -> Vector2:
        mag = self.length()
        if mag > 0:
            self.x /= mag
            self.y /= mag
        return self
    
    def baked(self) -> tuple[float, float]:
        return (self.x, self.y)
    

# Simple logging functionality. Maybe the method is a little stinky:

log_list = []

def log(*args: tuple) -> None:
    """Log function to allow logging across different modules"""
    global log_list

    t = formatted_time = datetime.now().strftime("%H:%M:%S:%f")[:-3]

    txt = ' '.join(str(arg) for arg in args)
    log_list.append(f"| {t} | {txt}")

def output_log() -> None:
    """Function to output latest log messages"""

    global log
    for txt in log:
        print(txt)
    log.clear()
