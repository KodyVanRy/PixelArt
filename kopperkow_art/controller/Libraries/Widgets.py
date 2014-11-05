import pygame, Shapes
from pygame.locals import *

__author__ = 'Kody'

class MenuButton(pygame.Surface):
    def __init__(self, location, size):
        pygame.Surface.__init__(self, (size))
        Shapes.drawOutsetRect(self)
        self.size = size
        self.location = location
        self.MODE = MOUSEBUTTONUP
    def update(self, event):
        if (self.inBounds(event.pos)):
            if event.type == MOUSEBUTTONDOWN:
                self.MODE = MOUSEBUTTONDOWN
                self.redraw(MOUSEBUTTONDOWN)
            elif event.type == MOUSEMOTION:
                self.MODE = MOUSEMOTION
                self.redraw(MOUSEMOTION)
            elif self.MODE == MOUSEBUTTONDOWN and event.type == MOUSEBUTTONUP:
                self.MODE = MOUSEBUTTONUP
                self.redraw(MOUSEBUTTONUP)
        elif self.MODE != MOUSEBUTTONUP:
            self.MODE = MOUSEBUTTONUP
            self.redraw(MOUSEBUTTONUP)