import pygame, MainController, sys
from pygame.locals import *
from Libraries import Colors, Sources, Widgets, Objects
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

        self.MENU = MenuBar(controller, ["File", "Edit", "Help", "Change Color"], [self.mainController.printHi, self.mainController.printHi, self.mainController.printHi, self.change_color], (width, 40))
        self.CANVAS = Canvas((8, 8), self.get_size(), self.MENU.get_size(), self.mainController)
        self.drawScreen()

    def showImage(self, image):
        self.fill((0,0,0))
        self.blit(image, (self.get_size()[0]/2 - image.get_size()[0]/2, self.get_size()[1]/2 - image.get_size()[1]/2))

    def update(self):
        for event in pygame.event.get():
            if self.visibleWindows != None:
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
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
                    self.drawScreen()
                elif event.type == MOUSEBUTTONUP:
                    self.MOUSE_IS_DOWN = False
                    self.updateMouseInput(event)
                elif event.type == MOUSEMOTION and self.MOUSE_IS_DOWN:
                    self.updateMouseInput(event)
                    self.drawScreen()
                elif event.type == MOUSEMOTION:
                    self.updateMouseInput(event)
    def updateKeyInput(self, event):
        print(pygame.key.name(event.key))

    def updateMouseInput(self, event):
        if (self.MENU.inBounds(event.pos)):
            self.MENU.update(event)
        else:
            self.CANVAS.update(event)

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
        self.blit(self.CANVAS, self.CANVAS.location)
        if self.visibleWindows != None:
            self.blit(self.visibleWindows, self.visibleWindows.location)
    def needsRedraw(self):
        if self.NEEDSREDRAW:
            self.NEEDSREDRAW = False
            return True
        else:
            return False

    def change_color(self):
        self.setVisibleWindow(PopupWindow(PopupWindow.COLOR_DIALOG, "Base Color", self.get_size(), self.mainController))

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
    def __init__(self, size, mainViewSize, menuSize, mainController):
        self.size = size
        self.color = Colors.BLACK
        mainViewSize = (mainViewSize[0], mainViewSize[1] - menuSize[1])
        self.cell_size = mainViewSize[1]/size[1]
        pygame.Surface.__init__(self, (self.size[0] * self.cell_size, self.size[1]*self.cell_size))
        self.location = ((mainViewSize[0]/2 - self.get_size()[0]/2), menuSize[1])
        self.MOUSEDOWN = False
        self.TILES = []
        self.redraw()
    def redraw(self):
        self.fill(Colors.WHITE)
        for x in range(1, self.size[0]):
            pygame.draw.line(self, Colors.DARK_GREY, (x * self.cell_size, 0), (x * self.cell_size, self.get_size()[1]))
        for y in range(1, self.size[1]):
            pygame.draw.line(self, Colors.DARK_GREY, (0, y * self.cell_size), (self.get_size()[0], y * self.cell_size))
        for tile in self.TILES:
            self.blit(tile, (tile.location[0]*self.cell_size, tile.location[1]*self.cell_size))
    def update(self, event):
        eventPos = (event.pos[0] - self.location[0], event.pos[1] - self.location[1])
        if event.type == MOUSEBUTTONDOWN: print eventPos
        if event.type == MOUSEBUTTONDOWN:
            self.MOUSEDOWN = True
            self.draw((eventPos[0]/self.cell_size, eventPos[1]/self.cell_size))
        elif event.type == MOUSEMOTION and self.MOUSEDOWN:
            self.draw((eventPos[0]/self.cell_size, eventPos[1]/self.cell_size))
        elif event.type == MOUSEBUTTONUP:
            self.MOUSEDOWN = False
            self.redraw()

    def draw(self, pos):
        newSurf = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
        newSurf.fill(self.color)
        self.blit(newSurf, (pos[0]*self.cell_size, pos[1]*self.cell_size))
        self.TILES.append(Objects.Tile(newSurf, pos))

    def setColor(self, color):
        self.color = color

class PopupWindow(pygame.Surface):
    YES_NO_DIALOG = "yndialog"
    OPTION_DIALOG = "optdialog"
    COLOR_DIALOG = "coldialog"
    def __init__(self, type, message, mainViewSize, mainController, options=[], entries=[]):
        self.type = type
        self.message = message
        self.mainController = mainController
        self.options = options
        self.entries = entries
        self.size = self.getSize()
        pygame.Surface.__init__(self, self.size)
        self.location = (mainViewSize[0]/2 - self.get_size()[0]/2, mainViewSize[1]/2 - self.get_size()[1]/2)
        self.title = Sources.TEXTBOX_FONT.render(self.message, 1, Colors.WHITE)
        self.title_location = (self.get_size()[0]/2 - self.title.get_size()[0]/2, 10)
        self.fill(Colors.DARK_GREY)
        #### ---- SETUP ALL WIDGETS ---- ####
        self.TEXT_BOXS = []
        self.BUTTONS = []
        if self.type == self.COLOR_DIALOG:
            self.setUpColorDialog()
        self.redraw()
    def update(self, event):
        for textbox in self.TEXT_BOXS:
            textbox.update(event)
        for button in self.BUTTONS:
            button.update(event)
    def redraw(self):
        if self.type == self.YES_NO_DIALOG:
            self.drawYNDIALOG()
        elif self.type == self.OPTION_DIALOG:
            self.drawOPTDIALOG()
        elif self.type == self.COLOR_DIALOG:
            self.drawCOLDIALOG()
    def drawYNDIALOG(self):
        #TODO
        pass
    def drawOPTDIALOG(self):
        #TODO
        pass
    def drawCOLDIALOG(self):
        self.fill(Colors.DARK_GREY)
        self.blit(self.title, self.title_location)
        for textbox in self.TEXT_BOXS:
            self.blit(textbox, textbox.location)
        for button in self.BUTTONS:
            self.blit(button, button.location)
    def getSize(self):
        #TODO fix this method getSize
        if self.type == self.YES_NO_DIALOG:
            return (200, 100)
        elif self.type == self.OPTION_DIALOG:
            return (200, 400)
        elif self.type == self.COLOR_DIALOG:
            return (400, 150)
    def setUpColorDialog(self):
        self.BUTTONS.append(Widgets.Button(self.mainController, (self.get_size()[0]/2 - 100, self.get_size()[1] - 50), (200, 40), "OK", self.setColor, Colors.WHITE, Colors.BLACK))
        self.TEXT_BOXS.append(Widgets.TextBox((self.get_size()[0]/2 - 50, self.get_size()[1] - 110), (100, 50), "WHAT?1?", "G", Widgets.TextBox.NUMBERS, self.mainController))
        self.TEXT_BOXS.append(Widgets.TextBox((self.TEXT_BOXS[0].location[0] - 110, self.get_size()[1] - 110), (100, 50), "W", "R", Widgets.TextBox.NUMBERS, self.mainController))
        self.TEXT_BOXS.append(Widgets.TextBox((self.TEXT_BOXS[0].location[0] + 110, self.get_size()[1] - 110), (100, 50), "W", "B", Widgets.TextBox.NUMBERS, self.mainController))
    def unfocusAllText(self):
        for textbox in self.TEXT_BOXS:
            textbox.HAS_FOCUS = False
    def setColor(self):
        try:
            if (int(self.TEXT_BOXS[0].getText()) > 255 or int(self.TEXT_BOXS[0].getText()) < 0):
                self.mainController.myView.visibleWindows = None
                return
            elif (int(self.TEXT_BOXS[1].getText()) > 255 or int(self.TEXT_BOXS[1].getText()) < 0):
                self.mainController.myView.visibleWindows = None
                return
            elif (int(self.TEXT_BOXS[2].getText()) > 255 or int(self.TEXT_BOXS[2].getText()) < 0):
                self.mainController.myView.visibleWindows = None
                return
            else:
                self.mainController.myView.CANVAS.setColor((int(self.TEXT_BOXS[0].getText()), int(self.TEXT_BOXS[1].getText()), int(self.TEXT_BOXS[2].getText())))
                self.mainController.myView.visibleWindows = None
                return
        except:
            self.mainController.myView.visibleWindows = None
            return
