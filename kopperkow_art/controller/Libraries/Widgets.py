import pygame, Shapes, Colors, Sources
from pygame.locals import *

__author__ = 'Kody'

class MenuButton(pygame.Surface):
    def __init__(self, mainController, location, size, text, isDropdown, command, options=[], commands=[]):
        pygame.Surface.__init__(self, (size))
        self.blit(Shapes.drawOutsetRect(self, size, 10, Colors.BACKGROUND, Colors.MENU_BUTTON_BACKGROUND), (0,0))
        self.mainController = mainController
        self.size = size
        self.location = location
        self.text = text
        self.command = command
        self.text = Sources.MENU_FONT.render(text, 1, Colors.MENU_BUTTON_TEXT_COLOR)
        self.text_location = (self.size[0]/2 - self.text.get_size()[0]/2, self.size[1]/2 - self.text.get_size()[1]/2)
        self.blit(self.text, self.text_location)
        self.MODE = MOUSEBUTTONUP
    def update(self, event):
        if (self.inBounds(event.pos)):
            if event.type == MOUSEBUTTONDOWN:
                self.redraw(MOUSEBUTTONDOWN)
                self.MODE = MOUSEBUTTONDOWN
            elif event.type == MOUSEMOTION:
                self.redraw(MOUSEMOTION)
                self.MODE = MOUSEMOTION
            elif self.MODE == MOUSEBUTTONDOWN and event.type == MOUSEBUTTONUP:
                self.command()
                self.redraw(MOUSEBUTTONUP)
                self.MODE = MOUSEBUTTONUP
        elif self.MODE != MOUSEBUTTONUP:
            self.redraw(MOUSEBUTTONUP)
            self.MODE = MOUSEBUTTONUP
    def redraw(self, type):
        if type == MOUSEMOTION and type != self.MODE:
            self.blit(Shapes.drawOutsetRect(self, self.get_size(), 10, Colors.LIGHT_BACKGROUND, Colors.MENU_BUTTON_BACKGROUND), (0,0))
            self.blit(self.text, self.text_location)
            self.mainController.myView.MENU.drawMenu()
            self.mainController.myView.drawScreen()
        elif type == MOUSEBUTTONUP and type != self.MODE:
            self.blit(Shapes.drawOutsetRect(self, self.get_size(), 10, Colors.BACKGROUND, Colors.MENU_BUTTON_BACKGROUND), (0,0))
            self.blit(self.text, self.text_location)
            self.mainController.myView.MENU.drawMenu()
            self.mainController.myView.drawScreen()
        elif type == MOUSEBUTTONDOWN and type != self.MODE:
            self.blit(Shapes.drawOutsetRect(self, self.get_size(), 10, Colors.DARK_GREY, Colors.MENU_BUTTON_BACKGROUND), (0,0))
            self.blit(self.text, self.text_location)
            self.mainController.myView.MENU.drawMenu()
            self.mainController.myView.drawScreen()
    def inBounds(self, pos):
        if (pos[0] >= self.location[0] and
            pos[0] <= self.location[0] + self.size[0] and
            pos[1] >= self.location[1] and
            pos[1] <= self.location[1] + self.size[1]):
            return True
        return False