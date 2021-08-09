import pygame
class ComponenteGeral():
    def __init__(self, window, x=0,y=0,w=0,h=0):
        self.window = window
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        
    def set_posicao(self,x,y):
        self.x = x
        self.y = y

    def draw(self):
        pass

    def evento(self,e):
        pass