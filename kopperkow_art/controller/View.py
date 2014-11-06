import pygame, MainController, sys
from pygame.locals import *
from Libraries import Colors, Sources, Widgets
from kopperkow_art.controller.Libraries.Widgets import MenuButton

__author__ = 'Kody'

class MainView(pygame.Surface):
    def __init__(self, width, height, controller):
        pygame.init()
        pygame.Surface.__init__(self, (width, height))
        self.MOUSE_IS_DOWN = False
        self.mainController = controller
        self.visibleWindows = None
        self.NEEDSREDRAW = True

        self.MENU = MenuBar(controller, ["File", "Edit", "Help"], [self.mainController.printHi, self.showImage, self.showImage], (width, 40))

        self.drawScreen()

    def showImage(self, image):
        self.fill((0,0,0))
        self.blit(image, (self.get_size()[0]/2 - image.get_size()[0]/2, self.get_size()[1]/2 - image.get_size()[1]/2))

    def update(self):
        for event in pygame.event.get():
            if self.visibleWindows != None:
                self.visibleWindows.update(event)
            else:
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    self.updateKeyInput(event)
                elif event.type == MOUSEBUTTONDOWN:
                    self.MOUSE_IS_DOWN = True
                    self.updateMouseInput(event)
                elif event.type == MOUSEBUTTONUP:
                    self.MOUSE_IS_DOWN = False
                    self.updateMouseInput(event)
                elif event.type == MOUSEMOTION:
                    self.updateMouseInput(event)
                    self.drawScreen()

    def updateKeyInput(self, event):
        print(event.key)

    def updateMouseInput(self, event):
        if (self.MENU.inBounds(event.pos)):
            self.MENU.update(event)

    def updateImage(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit();
                sys.exit();

    def setVisibleWindow(self, window):
        self.visibleWindows = window

    def drawScreen(self):
        self.NEEDSREDRAW = True
        self.fill(Colors.BACKGROUND)
        self.blit(self.MENU, (0,0))

    def needsRedraw(self):
        if self.NEEDSREDRAW:
            self.NEEDSREDRAW = False
            return True
        else:
            return False

class MenuBar(pygame.Surface):
    def __init__(self, mainController, options, commands, size):
        pygame.Surface.__init__(self, size)
        self.size = size
        self.mainController = mainController
        self.popUpMenu = None
        self.buttons = []
        self.options = options
        self.commands = commands

        self.setupButtons()

        self.drawMenu()
    def drawMenu(self):
        self.fill(Colors.MENU_BACKGROUND)
        for button in self.buttons:
            self.blit(button, button.location)

    def setupButtons(self):
        for x in range(len(self.options)):
            self.buttons.append(Widgets.MenuButton(self.mainController, (5 + (x * 110),5), (100, self.get_size()[1] - 10), self.options[x], False, self.commands[x]))

    def inBounds(self, pos):
        if (pos[1] <= self.size):
            return True
        return False

    def update(self, event):
        for button in self.buttons:
            button.update(event)

class MenuBarPopup(pygame.Surface):
    def __init__(self, mainController, size, options, commands=[]):
        self.size = size;
        self.mainController = mainController
        self.setupView(size, options, commands)
        self.commands = commands

    def setupView(self, options, commands):
        if self.size == "WRAP":
            print("TODO WRAP")
        else:
            pygame.Surface.__init__(self, self.size)