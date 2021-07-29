import pygame
from telas.telaGeral import TelaGeral
class MenuPrincipal(TelaGeral):
    def exibir(self):
        super().exibir()
        self.pygame.draw.rect(self.screen,(255,0,0),[0,0,100,100],0)
        