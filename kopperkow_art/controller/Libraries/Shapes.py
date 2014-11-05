import pygame
from pygame.locals import *

__author__ = 'Kody'

def drawOutsetRect(surf, size, outset, borderColor, color):
    """
    surf ->
    :rtype : pygame.Surface
    """
    surf.fill(color)
    a, b = color, borderColor
    rate = (
        float(b[0]-a[0])/size[1],
        float(b[1]-a[1])/size[1],
        float(b[2]-a[2])/size[1]
    )
    for line in range(outset):
        color = (
            min(max(a[0]+(rate[0]*(line-surf.get_rect().top)),0),255),
            min(max(a[1]+(rate[1]*(line-surf.get_rect().top)),0),255),
            min(max(a[2]+(rate[2]*(line-surf.get_rect().top)),0),255)
        )
        pygame.draw.rect(surf, color, (surf.get_rect()[0]+line,
                                       surf.get_rect()[1]+line,
                                       surf.get_rect()[2]-line*2,
                                       surf.get_rect()[3]-line*2))
    return surf
