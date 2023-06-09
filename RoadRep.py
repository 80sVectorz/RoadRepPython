""" RoadRep.py Main module. """
from copy import copy
from dataclasses import dataclass
from typing import TypedDict,Union
import typing
import numpy as np
from enum import Enum
from Utils import Vector2

class LaneShapeType(Enum):
    """The kind of a shape a Lane instance takes"""
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
        """Sets the Start & End line segment parameters of the Lane."""

        if self.shapeType != LaneShapeType.LINEAR:
            raise Exception(f"Set linear requires a road shape type of LINEAR | type found: {self.shapeType}")
        self.start = copy(start)
        self.end = copy(end)
 
    def set_linear_from_shape(self,shape: LinearShape) -> None:
        """Sets the Start & End line segment parameters of the Lane from a shape class."""

        self.set_linear(shape.start,shape.end)

    def lane_offset(self,lane: int) -> None:
        """Offsets the lane along it's normal based on the lane number given."""

        if self.shapeType == LaneShapeType.LINEAR:
            #Normal vector to offset the lane calculated using https://stackoverflow.com/questions/1243614/how-do-i-calculate-the-normal-vector-of-a-line-segment
            dx = self.end.x - self.start.x
            dy = self.end.y - self.start.y
            normal = Vector2(-dy,dx).normalized()

            #Off set the lane:
            self.start += normal*lane
            self.end += normal*lane

    def bake(self) -> None:
        """Bakes Vector2 type variables into tuples."""

        if self.shapeType == LaneShapeType.LINEAR:
            if self.start is Vector2:
                self.start = self.start.baked()
            if self.end is Vector2:
                self.end = self.end.baked()

class Road(Lane):
    def __init__(self, nLanes: int, shapeType: LaneShapeType, shape: Union[LinearShape,CurveShape]) -> None:
        if nLanes <= 0:
            raise Exception(f"Invalid nLanes for Road: {nLanes}")
        elif nLanes == 1:
            raise Warning("Road class used for single lane (nLanes == 1). It is recommended to use a normal lane class instead")
        self.nLanes = nLanes
        self.shapeType = shapeType
        self.shape = shape
        self.lanes = []
        self.build()

    def build(self) -> None:
        """Constructs the individual lanes based on the nLanes parameter."""

        self.lanes.clear()
        for i in range(self.nLanes):
            if self.shapeType == LaneShapeType.LINEAR:
                lane = Lane(LaneShapeType.LINEAR,self)
                lane.lane_offset(i)
                self.lanes.append(lane)

    def bake(self) -> None:
        """Calls the bake method on each child lane."""

        for lane in self.lanes:
            lane.bake()

class RoadNet:
    def __init__(self,segments: list[typing.Type["Lane"]]) -> None:
        self.segments = segments
        self.baked_lanes = []

    def bake(self) -> None:
        """
        Bakes higher level classes into simplest forms E.G Vector2 to tuple.
        Result gets written to the baked_lanes property.
        """

        self.baked_lanes.clear()
        for segment in self.segments:
            segment.bake()
            if type(segment) is Road:
                for lane in segment.lanes:
                    self.baked_lanes.append(lane)
            else:
                self.baked_lanes.append(segment)