# RoadRep.py Main module
from typing import List
import numpy as np
from enum import Enum
from Utils import Normalize

class RoadShapeType(Enum):
    LINEAR = 0
    CURVED = 1

class RoadShape:
    def __init__(self, shapeType: RoadShapeType) -> None:
        self.shapeType = shapeType
    def SetLinear(self, start: np.ndarray, end: np.ndarray) -> None:
        if self.shapeType != RoadShapeType.LINEAR:
            raise Exception(f"SetLINEAR requires a road shape type of LINEAR | type found: {self.shapeType}")
        self.start = start
        self.end = end
    def LaneOffset(self,lane: int):
        if self.shapeType == RoadShapeType.LINEAR:
            #Normal vector to offset the lane using https://stackoverflow.com/questions/1243614/how-do-i-calculate-the-normal-vector-of-a-line-segment
            dx = self.end[0] - self.start[0]
            dy = self.end[1] - self.start[1]
            normal = Normalize(np.array([-dx,dy]))
            #Off set the lane:
            self.start += normal*lane
            self.end += normal*lane

class Lane:
    def __init__(self,shape: RoadShape) -> None:
        self.shape = shape

class Road:
    def __init__(self,nLanes: int, shape: RoadShape) -> None:
        self.nLanes = nLanes
        self.shape = shape
        self.lanes = []
        for i in range(nLanes):
            if shape.shapeType == RoadShapeType.LINEAR:
                self.lanes.append(Lane(RoadShape(RoadShapeType.LINEAR)))
                self.lanes[i].shape.SetLinear(shape.start.copy(),shape.end.copy())
                self.lanes[i].shape.LaneOffset(i)

class RoadNet:
    def __init__(self,roads: List[Road]) -> None:
        self.roads = roads