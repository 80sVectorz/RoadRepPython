# RoadRep.py Main module
import numpy as np
from enum import Enum

class RoadShapeType(Enum):
    LINEAR = 0
    CURVED = 1


class RoadShape:
    def __init__(self, shapeType: RoadShapeType) -> None:
        self.shapeType = shapeType
    def SetLinear(self, start: np.ndarray, end: np.ndarray) -> None:
        if self.shapeType != RoadShapeType.LINEAR:
            raise Exception(f"SetLINEAR requires a road shape type of LINEAR | type found: {self.shapeType}")

class Lane:
    def __init__(self,start: np.ndarray,end: np.ndarray,road) -> None:
        self.start = start
        self.end = end

class Road:
    def __init__(self,nLanes: int, shape) -> None:
        pass