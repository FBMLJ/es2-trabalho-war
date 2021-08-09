from PPlay.window import *


class Texto:

    def __init__(self, janela: Window, texto: str, tamanho_da_fonte, cor):

        self.janela = janela
        self.x = 0
        self.y = 0
        self.texto = texto
        self.tamanho_da_fonte = tamanho_da_fonte
        self.cor = cor

    def draw(self):
        self.janela.draw_text(self.texto, self.x, self.y, self.tamanho_da_fonte, self.cor)

    def set_position(self, x, y):
        self.x = x
        self.y = y
