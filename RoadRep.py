# RoadRep.py Main module
from copy import copy
from dataclasses import dataclass
from typing import TypedDict,Union
import typing
import numpy as np
from enum import Enum
from Utils import Vector2

class LaneShapeType(Enum):
    """The kind of a shape a lane takes"""
    LINEAR = 0
    CURVED = 1

@dataclass
class LinearShape:
    start: Vector2
    end: Vector2

@dataclass
class CurveShape:
    #WIP
    start: Vector2
    end: Vector2


class Lane:
    def __init__(self, shapeType: LaneShapeType, inheritFrom: typing.Type["Lane"]=None) -> None:
        if inheritFrom:
            self.shapeType = inheritFrom.shapeType
            if self.shapeType == LaneShapeType.LINEAR:
                self.start = copy(inheritFrom.shape.start)
                self.end = copy(inheritFrom.shape.end)
        else:
            self.shapeType = shapeType

    def set_linear(self, start: Vector2, end: Vector2) -> None:
        if self.shapeType != LaneShapeType.LINEAR:
            raise Exception(f"Set linear requires a road shape type of LINEAR | type found: {self.shapeType}")
        self.start = copy(start)
        self.end = copy(end)
 
    def set_linear_from_shape(self,shape: LinearShape) -> None:
        self.set_linear(shape.start,shape.end) #This is efficient but it feels a little cursed

    def lane_offset(self,lane: int) -> None:
        if self.shapeType == LaneShapeType.LINEAR:
            #Normal vector to offset the lane calculated using https://stackoverflow.com/questions/1243614/how-do-i-calculate-the-normal-vector-of-a-line-segment
            dx = self.end.x - self.start.x
            dy = self.end.y - self.start.y
            normal = Vector2(-dy,dx).normalized()

            #Off set the lane:
            self.start += normal*lane
            self.end += normal*lane

    def bake(self) -> None:
        if self.shapeType == LaneShapeType.LINEAR:
            if self.start is Vector2:
                self.start = self.start.baked()
            if self.end is Vector2:
                self.end = self.end.baked()

class Road(Lane):
    def __init__(self, nLanes: int, shapeType: LaneShapeType, shape: Union[LinearShape,CurveShape]) -> None:
        self.nLanes = nLanes
        self.shapeType = shapeType
        self.shape = shape
        self.lanes = []
        self.build()

    def build(self) -> None:
        self.lanes.clear()
        for i in range(self.nLanes):
            if self.shapeType == LaneShapeType.LINEAR:
                lane = Lane(LaneShapeType.LINEAR,self)
                lane.lane_offset(i)
                self.lanes.append(lane)

    def bake(self) -> None:
        for lane in self.lanes:
            lane.bake()

class RoadNet:
    def __init__(self,segments: list[typing.Type["Lane"]]) -> None:
        self.segments = segments
        self.baked_lanes = []

    def bake(self) -> None:
        self.baked_lanes.clear()
        for segment in self.segments:
            segment.bake()
            if type(segment) is Road:
                for lane in segment.lanes:
                    self.baked_lanes.append(lane)
            else:
                self.baked_lanes.append(segment)