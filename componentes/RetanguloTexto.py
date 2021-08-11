import pygame
from PPlay.window import *
from componentes.Texto import *
from PPlay.mouse import *


class RetanguloTexto:

    def __init__(self, janela: Window, width=0, height=0, tamanho_texto=18, tamanho_maximo=10):

        self.janela = janela

        self.tamanho_maximo = tamanho_maximo

        self.x = 0
        self.y = 0
        self.width = width
        self.height = height

        self.texto = ""
        self.tamanho_texto = tamanho_texto

        self.retangulo_fora = pygame.Rect([self.x, self.y, self.width, self.height])
        self.retangulo_dentro = pygame.Rect([self.x, self.y, self.width, self.height])

        self.cor_ativa = (0, 0, 200)
        self.cor_inativa = (0, 0, 0)
        self.cor_atual = self.cor_inativa
        self.selecionado = False

        self.mouse = Mouse()

    def update(self):

        if self.mouse.is_over_area(
                (self.x, self.y),
                (self.x + self.width, self.y + self.height)
        ):
            self.cor_atual = self.cor_ativa
            if self.mouse.is_button_pressed(1):
                return True
        else:
            self.cor_atual = self.cor_inativa

        return False

    def render(self):

        if self.selecionado:
            self.cor_atual = self.cor_ativa

        pygame.draw.rect(self.janela.get_screen(), (255, 255, 255), self.retangulo_dentro)
        pygame.draw.rect(self.janela.get_screen(), self.cor_atual, self.retangulo_fora, 2)

        self.janela.draw_text(
            # Essa parte pega somente as letras que irão ser exibidas na tela
            self.texto[max(0, len(self.texto) - self.tamanho_maximo):],
            self.x + 5, self.y + self.height / 4, size=self.tamanho_texto, font_name="FreeMono, Monospace"
        )

    def set_position(self, x, y):
        self.retangulo_fora.update([self.x, self.y, self.width, self.height])
        self.retangulo_dentro.update([self.x, self.y, self.width, self.height])
