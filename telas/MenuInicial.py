"""
Classe responsavel por mostrar o menu inicial do jogo.
"""
from PPlay.window import *
from componentes.botao import *
from PPlay.gameimage import *
from constant import estados


class MenuInicial:

    def __init__(self, janela: Window):

        self.janela = janela

        self.fundo = GameImage("assets/imagem/tela_inicial/fundo.png")

        self.logo = GameImage("assets/imagem/tela_inicial/war.png")
        self.logo.set_position(
            self.janela.width/2-self.logo.width/2,
            self.janela.height/4-self.logo.height/2
        )

        self.botoes = []

        login_sprite_normal = Sprite("assets/imagem/tela_inicial/botao_login.png")
        login_sprite_destacado = Sprite("assets/imagem/tela_inicial/botao_login_select.png")
        botao_login = Botao(login_sprite_normal, login_sprite_destacado, estados["login"])
        self.botoes.append(botao_login)

        cadastro_sprite_normal = Sprite("assets/imagem/tela_inicial/botao_cadastro.png")
        cadastro_sprite_destacado = Sprite("assets/imagem/tela_inicial/botao_cadastro_select.png")
        botao_cadastro = Botao(cadastro_sprite_normal, cadastro_sprite_destacado, estados["cadastro"])
        self.botoes.append(botao_cadastro)

        partida_local_sprite_normal = Sprite("assets/imagem/tela_logado/botao_p_local.png")
        partida_local_sprite_destacado = Sprite("assets/imagem/tela_logado/botao_p_local_select.png")
        botao_partida_local = Botao(partida_local_sprite_normal, partida_local_sprite_destacado, estados["partida_local"])
        self.botoes.append(botao_partida_local)

        sair_sprite_normal = Sprite("assets/imagem/tela_inicial/botao_sair.png")
        sair_sprite_destacado = Sprite("assets/imagem/tela_inicial/botao_sair_select.png")
        botao_sair = Botao(sair_sprite_normal, sair_sprite_destacado, estados["sair"])
        self.botoes.append(botao_sair)

        # loop que calcula a posição de cada botão baseado na posição do anterior
        tamanho_acumulado = 0
        for index in range(len(self.botoes)):
            self.botoes[index].setposition(
                self.janela.width/2-self.botoes[index].width/2,
                self.janela.height / 2 + tamanho_acumulado + 100 + index*20
            )
            tamanho_acumulado += self.botoes[index].height

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
