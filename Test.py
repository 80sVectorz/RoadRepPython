# Test.py testing file

import colored_traceback
colored_traceback.add_hook()

import RoadRep
from RoadRep import LaneShapeType
from Utils import Vector2

lane = RoadRep.Lane(LaneShapeType.LINEAR)
lane.set_linear(Vector2(0,0),Vector2(0,10))