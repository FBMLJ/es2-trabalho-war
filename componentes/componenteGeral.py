import pygame
class ComponenteGeral():
    def __init__(self, window, x=0,y=0,w=0,h=0):
        self.window = window
        self.x = round(x*window.width/100)
        self.y = round(y*window.height/100)
        self.width = round(w*window.width/100)
        self.height = round(h*window.height/100)
        
    def set_posicao(self,x,y):
        self.x = round(x*self.window.width/100)
        self.y = round(y*self.window.height/100)

    def draw(self):
        pass

    def evento(self,e):
        pass