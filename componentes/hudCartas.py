from pygame import constants
from PPlay.window import Window
from componentes.botao import Botao
from PPlay.gameimage import GameImage
from PPlay.sprite import Sprite
from PPlay.mouse import Mouse
from jogo.Player import Player
from constant import *

class HudCartas:
    def __init__(self):
        #179 x 279

        self.botao_foi_clicado = False
        self.botao_clicado = None

        self.hud_trocas = None
        self.botao_mostrar_menu = None
        self.botoes = []

        self.cria()
        self.mostrar_cartas = False

        self.deve_trocar = False

    def update(self, mouse:Mouse):

        retorno = self.botao_mostrar_menu.update()
        if retorno:
            self.botao_foi_clicado = True
            self.botao_clicado = self.botao_mostrar_menu.code
        else:
            for botao in self.botoes:
                retorno = botao.update()
                if retorno:
                    self.botao_foi_clicado = True
                    self.botao_clicado = botao.code
        
        retorno = 0
        if self.botao_foi_clicado and not mouse.is_button_pressed(1):
            self.botao_foi_clicado = False
            if self.botao_clicado == 1: # Botao MOSTRAR MENU
                if not self.mostrar_cartas:
                    self.mostrar_cartas = True
            if self.botao_clicado == 2: # Botao OK
                retorno = self.botao_clicado
            if self.botao_clicado == 3: # Botao CANCELAR
                pass
            if self.botao_clicado == 4: # Botao VOLTAR
                self.mostrar_cartas = False
            if not self.deve_trocar:
                retorno = self.botao_clicado
            self.botao_clicado = 0
        
        return retorno

    def render(self, jogador:Player):
        self.botao_mostrar_menu.render()
        if self.mostrar_cartas:
            self.hud_trocas.draw()
            for botao in self.botoes:
                botao.render()
            self.desenha_cartas(jogador)

    def desenha_cartas(self, jogador:Player):
        dist_padrao = 48
        dist_vert = 42
        dist_acc = dist_padrao
        for carta in jogador.cartas:
            carta.img.set_position(
                self.hud_trocas.x + dist_acc,
                self.hud_trocas.y + dist_vert
            )
            carta.img.draw()
            dist_acc += carta.img.width + dist_padrao
    
    def cria(self):
        caminho_hud = "assets/imagem/hud/"
        self.mostrar_cartas = True
        self.deve_trocar = False

        self.hud_trocas = GameImage(caminho_hud + "barra_hud_card.png") #  Fundo para a exibicao das cartas
                                                                        #  Cabem 5 cartas com espacamento de 50 pixels
        self.hud_trocas.set_position(
            int(LARGURA_PADRAO/2) - int(self.hud_trocas.width/2),
            int(ALTURA_PADRAO/2) - int(self.hud_trocas.height/2)
        )

        self.botao_mostrar_menu = Botao(
            Sprite(caminho_hud + "botao_deck.png"), 
            Sprite(caminho_hud + "botao_deck_select.png"), 
            1
        )
        self.botao_mostrar_menu.setposition(
            LARGURA_PADRAO - int(1.1*self.botao_mostrar_menu.width),
            ALTURA_PADRAO - int(1.1*self.botao_mostrar_menu.height)
        )

        self.botoes = []

        botao_realizar_troca = Botao(Sprite(caminho_hud+"botao_ok.png"), Sprite(caminho_hud+"botao_ok_select.png"), 2)
        botao_realizar_troca.setposition(
            self.hud_trocas.x + int(0.25*self.hud_trocas.width) - int(botao_realizar_troca.width/2),
            self.hud_trocas.y + self.hud_trocas.height
        )
        self.botoes.append(botao_realizar_troca)

        botao_cancelar_troca = Botao(Sprite(caminho_hud+"botao_cancela.png"), Sprite(caminho_hud+"botao_cancela_select.png"), 3)
        botao_cancelar_troca.setposition(
            self.hud_trocas.x + int(0.5*self.hud_trocas.width) - int(botao_cancelar_troca.width/2),
            self.hud_trocas.y + self.hud_trocas.height
        )
        self.botoes.append(botao_cancelar_troca)
        
        botao_voltar_menu = Botao(Sprite(caminho_hud+"botao_retorna.png"), Sprite(caminho_hud+"botao_retorna_select.png"), 4)
        botao_voltar_menu.setposition(
            self.hud_trocas.x + int(0.75*self.hud_trocas.width) - int(botao_voltar_menu.width/2),
            self.hud_trocas.y + self.hud_trocas.height
        )
        self.botoes.append(botao_voltar_menu)

    def limpa(self):
        self.mostrar_cartas = False

        self.botao_foi_clicado = False
        self.botao_clicado = None

        self.hud_trocas = None
        self.botoes = []