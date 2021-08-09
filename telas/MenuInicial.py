"""
Classe responsavel por mostrar o menu inicial do jogo.
"""
from telas.ControladorJogo import *
from componentes.botao import *
from PPlay.gameimage import *


class MenuInicial:

    def __int__(self, janela: Window):

        self.janela = janela

        self.fundo = GameImage("assets/imagem/tela_inicial/fundo.png")

        self.logo = GameImage("assets/tela_inicial/war.png")


        self.botoes = []

        login_sprite_normal = Sprite("assets/imagem/tela_inicial/botao_login.png")
        login_sprite_destacado = Sprite("assets/imagem/tela_inicial/botao_login_select.png")
        botao_login = Botao(login_sprite_normal, login_sprite_destacado, 2)
        self.botoes.append(botao_login)

        convidado_sprite_normal = Sprite("assets/imagem/tela_inicial/botao_convidado.png")
        convidado_sprite_destacado = Sprite("assets/imagem/tela_inicial/botao_convidado_select.png")
        botao_convidado = Botao(convidado_sprite_normal, convidado_sprite_destacado, 3)
        self.botoes.append(botao_convidado)

        sair_sprite_normal = Sprite("assets/imagem/tela_inicial/botao_sair.png")
        sair_sprite_destacado = Sprite("assets/imagem/tela_inicial/botao_sair_select.png")
        botao_sair = Botao(sair_sprite_normal, sair_sprite_destacado, 4)
        self.botoes.append(botao_sair)

    def loop(self):

        self.janela.clear()
        mouse = Mouse()
        mouse_foi_clicado = False  # variavel que impede que o usuário clique várias vezes
        botao_clicado = 0

        while True:

            for botao in self.botoes:
                clicou = botao.update()
                if clicou:
                    mouse_foi_clicado = True #bloqueia o botao de ser clicado
                    botao_clicado = botao.code

            if mouse_foi_clicado and not mouse.is_button_pressed(1):  # evitar que seja clicados diversas vezes
                return botao_clicado

            self.render()
            self.janela.update()

    def render(self):
        self.fundo.draw()
        self.logo.draw()
        for botao in self.botoes:
            botao.render()
