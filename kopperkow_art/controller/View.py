import pygame, MainController, sys
from pygame.locals import *
from Libraries import Colors, Sources

__author__ = 'Kody'

class MainView(pygame.Surface):
    def __init__(self, width, height, controller):
        pygame.init()
        pygame.Surface.__init__(self, (width, height))
        self.MOUSE_IS_DOWN = False
        self.mainController = controller
        self.visibleWindows = None
        self.NEEDSREDRAW = True

        self.MENU = MenuBar(controller, (width, 40))

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
                elif event.type == MOUSEMOTION and self.MOUSE_IS_DOWN:
                    self.updateMouseInput(event)
                    self.drawScreen()

    def updateKeyInput(self, event):
        print(event.key)

    def updateMouseInput(self, event):
        if (self.MENU.inBounds(event.pos)):
            print("in menu")
        print(event.pos)

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
    def __init__(self, mainController, size):
        pygame.Surface.__init__(self, size)
        self.size = size
        self.mainController = mainController
        self.popUpMenu = None
        self.options = ["File", "Edit", "Help"]

        self.drawMenu()
    def drawMenu(self):
        self.fill(Colors.MENU_BACKGROUND)
        buttonSurf = pygame.Surface((100, 30))
        buttonSurf.fill(Colors.MENU_BUTTON_BACKGROUND)
        buttonText = Sources.MENU_FONT.render(self.options[0], 1, Colors.MENU_BUTTON_TEXT_COLOR)
        buttonSurf.blit(buttonText, (buttonSurf.get_size()[0]/2 - buttonText.get_size()[0]/2, buttonSurf.get_size()[1]/2 - buttonText.get_size()[1]/2))
        self.blit(buttonSurf, (5, 5))

    def inBounds(self, pos):
        if (pos[1] <= self.size):
            return True
        return False

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