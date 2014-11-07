import pygame, Shapes, Colors, Sources, string
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
        self.isDropdown = isDropdown
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

class TextBox(pygame.Surface):
    NUMBERS = "nums"
    def __init__(self, location, size, text, hint, inputType, mainController):
        pygame.Surface.__init__(self, (size))
        self.blit(Shapes.drawOutsetRect(self, size, 10, Colors.BACKGROUND, Colors.MENU_BUTTON_BACKGROUND), (0,0))
        self.size = size
        self.location = location
        self.fillerText = text
        self.hint = hint
        self.text = text
        self.asciiText = []
        self.text = Sources.MENU_FONT.render(text, 1, Colors.MENU_BUTTON_TEXT_COLOR)
        self.text_location = (self.size[0]/2 - self.text.get_size()[0]/2, self.size[1]/2 - self.text.get_size()[1]/2)
        self.blit(self.text, self.text_location)
        self.mainController = mainController
        self.MODE = MOUSEBUTTONUP
        self.ON_OFF_COUNTER = 0
        self.HAS_FOCUS = False
        self.redraw(False)
    def update(self, event):
        self.ON_OFF_COUNTER += 1
        if (self.ON_OFF_COUNTER == 20): self.ON_OFF_COUNTER = 0
        if event.type == KEYDOWN and self.HAS_FOCUS:
            if (pygame.key.name(event.key) in list(string.digits)):
                self.asciiText.append(pygame.key.name(event.key))
                self.redraw(True)
                return
        elif (event.type == MOUSEBUTTONDOWN and self.inBounds((event.pos[0] - self.mainController.myView.visibleWindows.location[0],
                                                               event.pos[1] - self.mainController.myView.visibleWindows.location[1]))):
            if event.type == MOUSEBUTTONDOWN:
                self.mainController.myView.visibleWindows.unfocusAllText()
                self.HAS_FOCUS = True
                self.mainController.myView.visibleWindows.redraw()
                self.redraw(True)
        else:
            if self.ON_OFF_COUNTER == 10:
                self.redraw(True)
            elif self.ON_OFF_COUNTER == 0:
                self.redraw(True)
    def redraw(self, doText):
        self.fill(Colors.TEXT_BOX_BACKGROUND)
        pygame.draw.rect(self, Colors.TEXT_BOX_OUTLINE, (0, 0, self.get_size()[0], self.get_size()[1]), 4)
        self.fill(Colors.TEXT_BOX_BACKGROUND, (0, 0, self.get_size()[0], self.get_size()[1]-10))
        self.text = self.text = Sources.TEXTBOX_FONT.render("".join(self.asciiText) + ("|" if self.HAS_FOCUS else ""), 1, Colors.WHITE)
        self.text_location = (self.size[0]/2 - self.text.get_size()[0]/2, self.size[1]/2 - self.text.get_size()[1]/2)
        self.blit(self.text, self.text_location)
        if (doText):
            self.mainController.myView.visibleWindows.redraw()
            self.mainController.myView.drawScreen()
    def inBounds(self, pos):
        if (pos[0] >= self.location[0] and
            pos[0] <= self.location[0] + self.size[0] and
            pos[1] >= self.location[1] and
            pos[1] <= self.location[1] + self.size[1]):
            return True
        return False
    def getText(self):
        return "".join(self.asciiText)

class Button(pygame.Surface):
    def __init__(self, mainController, location, size, text, command, insideColor, outsideColor):
        pygame.Surface.__init__(self, (size))
        self.blit(Shapes.drawOutsetRect(self, size, 10, insideColor, outsideColor), (0,0))
        self.insideColor = insideColor
        self.outsideColor = outsideColor
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
        if event.type not in (MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION):
            return
        if (self.inBounds((event.pos[0] - self.mainController.myView.visibleWindows.location[0],
                           event.pos[1] - self.mainController.myView.visibleWindows.location[1]))):
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
            self.blit(Shapes.drawOutsetRect(self, self.get_size(), 10, self.insideColor, self.outsideColor), (0,0))
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