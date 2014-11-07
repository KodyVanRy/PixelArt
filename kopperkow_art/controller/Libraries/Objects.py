import pygame
from pygame.locals import *

__author__ = 'Kody'

pygame.init()

class Tile(pygame.Surface):
    def __init__(self, surface, loc):
        pygame.Surface.__init__(self, surface.get_size())
        self.blit(surface, (0,0))
        self.color = color
        self.location = loc