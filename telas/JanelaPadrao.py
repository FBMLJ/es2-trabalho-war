import pygame
class JanelaPadrao:

    def __init__(self, janela):
        self.janela = janela
        self.pygame = pygame


    def trataEvento(self):
        for e in pygame.event.get():
            self.evento(e)
    
    def evento(self):
        pass

    def draw(self):
        self.trataEvento()