from typing import Text
from componentes.componenteGeral import ComponenteGeral
import pygame
from PPlay.mouse import Mouse


class CampoTexto(ComponenteGeral):
    def __init__(self, window, titulo: str, x=0, y=0, w=0, h=0,tamanho_maximo=24, tamanho_titulo=18):
        super().__init__(window, x, y, w, h)

        self.titulo = titulo
        self.retango_fora = pygame.Rect([self.x, self.y, self.width, self.height])
        self.retango_dentro = pygame.Rect([self.x, self.y, self.width, self.height])
        self.texto = ""
        self.tamanho_maximo = tamanho_maximo
        self.size = round((self.height)/2)
        self.tamanho_titulo = tamanho_titulo
        self.cor_ativa = (0, 0, 200)
        self.cor_inativa = (0, 0, 0)
        self.cor = self.cor_inativa
        self.ativo = False
        self.mouse = Mouse()


    def draw(self):
        super().draw()
        #branco do campo de texto
        pygame.draw.rect(self.window.get_screen(), (255,255,255),self.retango_dentro)
        #borda do campo de texto
        pygame.draw.rect(self.window.get_screen(), self.cor,self.retango_fora, 2)
        
        self.window.draw_text( #desenha o título do campo
            self.titulo,
            self.x,
            self.y - self.tamanho_titulo - 5,
            self.tamanho_titulo,
            [0, 0, 0],
            font_name = "FreeMono, Monospace",
            bold = True
        )
        self.window.draw_text(
            # Essa parte pega somente as letras que irão ser exibidas na tela
            self.texto[max(0,len(self.texto)-self.tamanho_maximo):], 
        self.x+5,self.y+self.height/4, size = self.size, font_name ="FreeMono, Monospace")


    def evento(self, e):
        super().evento(e)
        if self.ativo:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_BACKSPACE:
                    self.texto = self.texto[:-1]
                elif e.key == pygame.K_RETURN:
                    self.ativo = False
                    self.cor = self.cor_inativa
                else:
                    self.texto += e.unicode
            elif e.type == pygame.MOUSEBUTTONDOWN and not self.retango_fora.collidepoint(self.mouse.get_position()):
                    self.ativo = False
                    self.cor = self.cor_inativa
                    
        else:
            if e.type == pygame.MOUSEBUTTONDOWN:
                if self.retango_fora.collidepoint(self.mouse.get_position()):
                    self.ativo = True
                    self.cor = self.cor_ativa