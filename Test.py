# Test.py testing file

import colored_traceback
colored_traceback.add_hook()

from numpy import array as nparray;
import RoadRep
from RoadRep import RoadShapeType

shape = RoadRep.RoadShape(RoadShapeType.CURVED)
shape.SetLinear(nparray([1,2]),nparray([3,4]))