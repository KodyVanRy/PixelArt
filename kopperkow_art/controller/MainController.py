import  sys, pygame
from View import  MainView
from pygame.locals import *

__author__ = 'Kody'

pygame.init()

VIEW_WIDTH = 960
VIEW_HEIGHT = 580
DISPLAYSURF = pygame.display.set_mode((VIEW_WIDTH, VIEW_HEIGHT))
FPSCLOCK = pygame.time.Clock()
FPS = 40

showingImage = False

class MainController:
    def __init__(self, inFile="", outFile="", viewOnly=False):
        self.myView = MainView(VIEW_WIDTH, VIEW_HEIGHT, self)
        if viewOnly:
            showingImage = True
            self.myView.showImage(inFile)
        self.run()

    def run(self):
        while True:
            FPSCLOCK.tick(FPS)
            if (FPSCLOCK.get_fps() < 30):
                print("Running slow...\nFPS: " + str(FPSCLOCK.get_fps()))
            if (showingImage):
                self.myView.updateImage()
            else:
                self.myView.update()
                if self.myView.needsRedraw():
                    DISPLAYSURF.blit(self.myView, (0,0))
                    pygame.display.update()
    def printHi(self):
        print('hi')