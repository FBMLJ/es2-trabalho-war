import pygame
class ComponenteGeral():
    def __init__(self, window, x,y,w,h):
        self.window = window
        self.x = round(x*window.width)
        self.y = round(y*window.height)
        self.x = round(w*window.width)
        self.y = round(h*window.height)
        
    def set_posicao(self,x,y):
        self.x = round(x*self.window.width)
        self.y = round(y*self.window.height)