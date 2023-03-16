# RoadRepViewer.py A simple view application used for debugging.
# made using this template: https://gist.github.com/MatthewJA/7544830

import RoadRep
import sys
import numpy as np
from Utils import Vector2
 
import pygame
from pygame.locals import *

# Function definitions:
def WorldToScreen(p: np.ndarray) -> np.ndarray:
  return (p*(Vector2(width,height)/frustum)*Vector2(1,-1)) + Vector2(width/2,height/2)

def ScreenToWorld(p: np.ndarray,camPos: np.ndarray) -> np.ndarray:
  return (p - Vector2(width/2,height/2))/((Vector2(width,height)/frustum)*Vector2(1,-1))+camPos

def UpdateFrustum(zoom: int) -> np.ndarray:
  return Vector2(zoom,zoom/screenRatio)

pygame.init()

fps = 60
fpsClock = pygame.time.Clock()
 
width, height = 640, 480
screenRatio = width/height
screen = pygame.display.set_mode((width, height))


# Test road network:
shape = RoadRep.RoadShape(RoadRep.RoadShapeType.LINEAR)
shape.SetLinear(Vector2(0,0),Vector2(50,40))
roads = [RoadRep.Road(4,shape)]
rn = RoadRep.RoadNet(roads)

# runtime variables:
zoom = 500
frustum = Vector2(zoom,zoom/screenRatio)
camPos = Vector2(0.0,0.0)
panning = False
panStartPos = Vector2(0.0,0.0)
panStartCamPos = camPos

# program loop:
while True:
  screen.fill((0, 0, 0))

  # Event handling & Updates:
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit() 
    # Zooming:
    if event.type == pygame.MOUSEWHEEL:
      scrollChange = event.y
      mousePos = pygame.mouse.get_pos()
      mouseBeforePos = ScreenToWorld(np.array(mousePos),camPos)
      zoom-=scrollChange*10
      zoom=max(zoom,10)
      frustum = UpdateFrustum(zoom)
      mouseAfterPos = ScreenToWorld(mousePos,camPos)
      camPos-=mouseBeforePos-mouseAfterPos

  # Panning:
  mouseButton = pygame.mouse.get_pressed(3)[0]
  if mouseButton and not panning:
    panStartCamPos = camPos
    print("camPos:",camPos)
    panStartPos = ScreenToWorld(np.array(pygame.mouse.get_pos()),panStartCamPos)
    panning = True
  elif mouseButton and panning:
    camPos=panStartCamPos+(ScreenToWorld(np.array(pygame.mouse.get_pos()),panStartCamPos)-panStartPos)
  elif not mouseButton and panning:
    panning = False
  
  
  # Draw:
  for road in rn.roads:
    for lane in road.lanes:
      if lane.shape.shapeType == RoadRep.RoadShapeType.LINEAR:
        pygame.draw.line(screen,
                         (0,255,0),
                         WorldToScreen(lane.shape.start+camPos),
                         WorldToScreen(lane.shape.end+camPos))
  
  pygame.display.flip()
  fpsClock.tick(fps)