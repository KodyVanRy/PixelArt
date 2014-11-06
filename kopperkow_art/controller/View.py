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
        self.CANVAS = Canvas((5, 5), (self.get_size()[0], self.get_size()[1]-self.MENU.size[1]), self.mainController)
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
            print("in")
            self.MENU.update(event)
        else:
            print("0K...")
            self.CANVAS.update(event)
            print("hmm")

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
        self.blit(self.CANVAS, (self.get_size()[0]/2 - self.CANVAS.get_size()[0]/2, self.get_size()[1] - self.CANVAS.get_size()[1]))

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
        if (pos[1] <= self.size[1]):
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

class Canvas(pygame.Surface):
    def __init__(self, size, mainViewSize, mainController):
        self.size = size
        self.color = Colors.BLACK
        self.cell_size = mainViewSize[1]/size[1]
        pygame.Surface.__init__(self, (self.size[0] * self.cell_size, self.size[1]*self.cell_size))
        self.location = ((mainViewSize[0]/2 - self.get_size()[0]/2), (mainViewSize[1] - self.get_size()[1]))
        self.MOUSEDOWN = False
        self.redraw()
    def redraw(self):
        self.fill(Colors.WHITE)
        for x in range(1, self.size[0]):
            pygame.draw.line(self, Colors.DARK_GREY, (x * self.cell_size, 0), (x * self.cell_size, self.get_size()[1]))
        for y in range(1, self.size[1]):
            pygame.draw.line(self, Colors.DARK_GREY, (0, y * self.cell_size), (self.get_size()[0], y * self.cell_size))

    def update(self, event):
        eventPos = (event.pos[0] - self.location[0], event.pos[1] - self.location[1])
        if event.type == MOUSEBUTTONDOWN:
            self.MOUSEDOWN = True
            self.draw((eventPos[0]/self.cell_size, eventPos[1]/self.cell_size))

    def draw(self, pos):
        newSurf = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
        newSurf.fill(self.color)
        print("Draw")
        self.blit(newSurf, (pos[0]*self.cell_size, pos[1]*self.cell_size))

