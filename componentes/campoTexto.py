from typing import Text
from  componentes.componenteGeral import ComponenteGeral
import pygame
class CampoTexto(ComponenteGeral):
    def __init__(self, window, x=0, y=0, w=0, h=0,size = 24):
        super().__init__(window, x, y, w, h)
        self.retango_fora = pygame.Rect([self.x,self.y,self.width,self.height])
        self.retango_dentro = pygame.Rect([self.x,self.y,self.width,self.height])
        self.texto = ""
        self.size = size


    def draw(self):
        super().draw()
        pygame.draw.rect(self.window.get_screen(), (255,255,255),self.retango_dentro)
        pygame.draw.rect(self.window.get_screen(), (0,0,0),self.retango_fora, 1)
        
        self.window.draw_text(self.texto, self.x+5,self.y+self.height/4, size = self.size)


    def evento(self, e):
        super().evento(e)
        if e.type  == pygame.KEYDOWN:
            if e.key == pygame.K_BACKSPACE:
                self.texto = self.texto[:-1]
            else:
                self.texto += e.unicode
                print(self.texto)