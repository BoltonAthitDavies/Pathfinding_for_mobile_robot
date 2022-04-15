import pygame
from RRTbase_mod import RRTGraph
from RRTbase_mod import RRTMap
import time

def oreo():
    clock = pygame.time.Clock()
    map = pygame.display.set_mode((800, 600))
    grey = (70, 70, 70)
    white = (255, 255, 255)
    #a = pygame.draw.rect(map, grey, [400,300,10,10])
    pygame.display.set_caption("Experiment")

    #while loop
    state = True
    while state:
          for event in pygame.event.get():
                if event.type == pygame.QUIT:
                      state = False

          map.fill(white)

          #Filled rectangle
          X=100; Y=120; width=50; height=50
          pygame.draw.rect(map, grey, (X, Y, width, height))

          pygame.display.update()
          #clock.tick(30)
    return pygame.display.update()

print(oreo())

