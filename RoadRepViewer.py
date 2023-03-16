# RoadRepViewer.py A simple view application used for debugging.
# made using this template: https://gist.github.com/MatthewJA/7544830
import RoadRep
import sys
import numpy as np
from Utils import Vector2
 
import pygame
from pygame.locals import *
 
pygame.init()

fps = 60
fpsClock = pygame.time.Clock()
 
width, height = 640, 480
screenRatio = width/height
frustum = Vector2(500,500/screenRatio)
screen = pygame.display.set_mode((width, height))

def PointToScreen(p: np.ndarray):
  return (p*(Vector2(width,height)/frustum)*Vector2(1,-1)) + Vector2(width/2,height/2)

#Test road network:
shape = RoadRep.RoadShape(RoadRep.RoadShapeType.LINEAR)
shape.SetLinear(Vector2(0,0),Vector2(50,40))
roads = [RoadRep.Road(4,shape)]
rn = RoadRep.RoadNet(roads)

#runtime variables:
camPos = Vector2(0,0)
panning = False
panStartPos = Vector2(0,0)
panStartCamPos = camPos

# program loop.
while True:
  screen.fill((0, 0, 0))
  
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit() 
  # Update.
  mouseButton = pygame.mouse.get_pressed(3)[0]
  if mouseButton and not panning:
    panStartCamPos = camPos
    panStartPos = np.array(pygame.mouse.get_pos())
    panning = True
  elif mouseButton and panning:
    camPos=panStartCamPos+(np.array(pygame.mouse.get_pos())-panStartPos)
  elif not mouseButton and panning:
    panning = False
  
  # Draw.
  for road in rn.roads:
    for lane in road.lanes:
      if lane.shape.shapeType == RoadRep.RoadShapeType.LINEAR:
        pygame.draw.line(screen,
                         (0,255,0),
                         PointToScreen(lane.shape.start)+camPos,
                         PointToScreen(lane.shape.end)+camPos)
  
  pygame.display.flip()
  fpsClock.tick(fps)