"""
RoadRepViewer.py A simple view application used for debugging.
Made using this template: https://gist.github.com/MatthewJA/7544830
"""

import RoadRep
import sys
import argparse
import numpy as np
from Utils import Vector2
from Utils import log,output_log
import pygame
from pygame.locals import *

# Function definitions:
def WorldToScreen(p: Vector2, frustum: Vector2, width: int, height: int) -> Vector2:
  """Returns the converted world space P to screen space."""
  return (p*(Vector2(width,height)/frustum)*Vector2(1,-1)) + Vector2(width/2,height/2)

def ScreenToWorld(p: Vector2,camPos: Vector2, frustum: Vector2, width: int, height: int) -> Vector2:
  """Returns the converted screen space P to world space."""
  return (p - Vector2(width/2,height/2))/((Vector2(width,height)/frustum)*Vector2(1,-1))+camPos

def UpdateFrustum(zoom: int, screen_ratio: float) -> Vector2:
  """Returns the given frustum with the zoom applied."""
  return Vector2(zoom,zoom/screen_ratio)

def main():
  """Runs the program loop for RoadRepViewer.py."""

  # Argument handling:
  parser = argparse.ArgumentParser()
  parser.add_argument("-v","--verbose",dest="verbose",action="store_true",help="get debug info.")

  args = parser.parse_args()

  pygame.init()

  fps = 60
  fps_clock = pygame.time.Clock()
  
  width, height = 640, 480
  screen_ratio = width/height
  screen = pygame.display.set_mode((width, height))


  # Test road network:
  log("Creating test network.")

  roads = []
  shape = RoadRep.LinearShape(Vector2(0,0),Vector2(50,40))
  roads.append(RoadRep.Road(4,RoadRep.LaneShapeType.LINEAR,shape))
  shape = RoadRep.LinearShape(Vector2(10,30),Vector2(50,40))
  roads.append(RoadRep.Road(4,RoadRep.LaneShapeType.LINEAR,shape))

  rn = RoadRep.RoadNet(roads)
  rn.bake()
  log("Finished creating test network.")

  # Runtime variables:
  zoom = 500
  frustum = Vector2(zoom,zoom/screen_ratio)
  cam_pos = Vector2(0.0,0.0)
  panning = False
  pan_start_pos = Vector2(0.0,0.0)
  pan_start_cam_pos = cam_pos

  # Program loop:
  log("Starting main program loop.")

  while True:
    screen.fill((0, 0, 0))

    # Event handling & Updates:
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit() 
      # Zooming:
      if event.type == pygame.MOUSEWHEEL:
        scroll_change = event.y
        mouse_pos = pygame.mouse.get_pos()
        mouse_before_pos = ScreenToWorld(np.array(mouse_pos),cam_pos,frustum,width,height)
        zoom-=scroll_change*10
        zoom=max(zoom,10)
        frustum = UpdateFrustum(zoom,screen_ratio)
        mouse_after_pos = ScreenToWorld(np.array(mouse_pos),cam_pos,frustum,width,height)
        cam_pos-=mouse_before_pos-mouse_after_pos

    # Panning:
    mouse_button = pygame.mouse.get_pressed(3)[0]
    if mouse_button and not panning:
      pan_start_cam_pos = cam_pos
      pan_start_pos = ScreenToWorld(np.array(pygame.mouse.get_pos()),pan_start_cam_pos,frustum,width,height)
      panning = True
    elif mouse_button and panning:
      cam_pos=pan_start_cam_pos+(ScreenToWorld(np.array(pygame.mouse.get_pos()),pan_start_cam_pos,frustum,width,height)-pan_start_pos)
    elif not mouse_button and panning:
      panning = False
    
    
    # Draw:
    for lane in rn.baked_lanes:
          if lane.shapeType == RoadRep.LaneShapeType.LINEAR:
            pygame.draw.line(screen,
                            (0,255,0),
                            WorldToScreen(lane.start+cam_pos,frustum,width,height).baked(),
                            WorldToScreen(lane.end+cam_pos,frustum,width,height).baked())
    if args.verbose:
      output_log()  
    pygame.display.flip()
    fps_clock.tick(fps)
  
if __name__ == "__main__":
  main()