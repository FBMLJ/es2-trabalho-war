from PPlay.gameimage import *
from PPlay.window import *
from PPlay.sprite import *
import pygame
from componentes.campoTexto import *
from componentes.botao import *


class BuscaSaguao:

    def __init__(self, janela: Window, usuario: str):

        self.janela = janela
        self.fundo = GameImage("assets/imagem/busca_saguao/buscador_saguao.png")
        self.fundo.set_position(janela.width/2 - self.fundo.width/2, janela.height/2 - self.fundo.height/2)

        self.busca_pelo_nome = 1
        self.entrar = 2
        self.criar_partida = 3

        self.botoes = []

        buscar_saguao_sprite_normal = Sprite("assets/imagem/busca_saguao/botao_buscar.png")
        buscar_saguao_sprite_destacado = Sprite("assets/imagem/busca_saguao/busca_saguao_select.png")
        botao_busca_saguao = Botao(buscar_saguao_sprite_normal, buscar_saguao_sprite_destacado, self.busca_pelo_nome)
        botao_busca_saguao.setposition(
            self.fundo.x + 30,
            self.fundo.y + self.fundo.height - self.janela.height*0.17
        )
        self.botoes.append(botao_busca_saguao)

        entrar_saguao_sprite_normal = Sprite("assets/imagem/busca_saguao/botao_entrar.png")
        entrar_saguao_sprite_destacado = Sprite("assets/imagem/busca_saguao/botao_entrar_select.png")
        botao_entrar_saguao = Botao(entrar_saguao_sprite_normal, entrar_saguao_sprite_destacado, self.entrar)
        botao_entrar_saguao.setposition(
            self.fundo.x + 30,
            self.fundo.y + self.fundo.height - self.janela.height*0.10
        )
        self.botoes.append(botao_entrar_saguao)

        criar_saguao_sprite_normal = Sprite("assets/imagem/busca_saguao/botao_criar.png")
        criar_saguao_sprite_destacado = Sprite("assets/imagem/busca_saguao/botao_criar_select.png")
        botao_criar_saguao = Botao(criar_saguao_sprite_normal, criar_saguao_sprite_destacado, self.criar_partida)
        botao_criar_saguao.setposition(
            self.fundo.x + self.fundo.width - criar_saguao_sprite_destacado.width - self.janela.width*0.055,
            self.fundo.y + self.fundo.height - self.janela.height*0.10
        )
        self.botoes.append(botao_criar_saguao)

        self.campo_busca_saguao = CampoTexto(
            janela,
            self.fundo.x + 30,
            self.fundo.y + self.fundo.height - self.janela.height*0.28,
            self.janela.width * 0.23,
            self.janela.height * 0.06
        )

        self.campo_nome_sala = CampoTexto(
            janela,
            self.fundo.x + self.fundo.width - self.janela.width * 0.15 - self.janela.width*0.04,
            self.fundo.y + self.fundo.height - self.janela.height * 0.28,
            self.janela.width * 0.15,
            self.janela.height * 0.05
        )

        self.campo_senha_sala = CampoTexto(
            janela,
            self.fundo.x + self.fundo.width - self.janela.width * 0.15 - self.janela.width*0.04,
            self.fundo.y + self.fundo.height - self.janela.height * 0.20,
            self.janela.width * 0.15,
            self.janela.height * 0.05
        )

        self.saguoes = []

    def loop(self):

        self.janela.clear()
        mouse_foi_clicado = False
        mouse = Mouse()
        self.janela.input_pygame = True

        while True:

            for botao in self.botoes:
                clicou = botao.update()
                if clicou:
                    mouse_foi_clicado = True  # bloqueia o botao de ser clicado
                    botao_clicado = botao.code

            if mouse_foi_clicado and not mouse.is_button_pressed(1):
                

            self.trataEvento()
            self.render()
            self.janela.update()

    def render(self):

        self.janela.set_background_color([0, 0, 0])
        self.fundo.draw()
        self.campo_busca_saguao.draw()
        self.campo_nome_sala.draw()
        self.campo_senha_sala.draw()
        for botao in self.botoes:
            botao.render()

    def trataEvento(self):

        for evento in pygame.event.get():
            self.campo_busca_saguao.evento(evento)
            self.campo_nome_sala.evento(evento)
            self.campo_senha_sala.evento(evento)
            if evento.type == pygame.QUIT:
                exit()
