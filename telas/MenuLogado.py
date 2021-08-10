"""
Classe responsavel por mostrar o menu quando o jogador estiver logado com sucesso.
"""
from PPlay.window import *
from componentes.botao import *
from PPlay.gameimage import *
from constant import estados


class MenuLogado:

    def __init__(self, janela: Window):

        self.janela = janela

        self.fundo = GameImage("assets/imagem/tela_inicial/fundo.png")

        self.logo = GameImage("assets/imagem/tela_inicial/war.png")
        self.logo.set_position(
            self.janela.width/2-self.logo.width/2,
            self.janela.height/4-self.logo.height/2
        )

        self.botoes = []

        partida_online_sprite_normal = Sprite("assets/imagem/tela_logado/botao_p_online.png")
        partida_online_sprite_destacado = Sprite("assets/imagem/tela_logado/botao_p_online_select.png")
        botao_partida_online = Botao(partida_online_sprite_normal, partida_online_sprite_destacado, estados["buscar_sala"])
        self.botoes.append(botao_partida_online)

        partida_local_sprite_normal = Sprite("assets/imagem/tela_logado/botao_p_local.png")
        partida_local_sprite_destacado = Sprite("assets/imagem/tela_logado/botao_p_local_select.png")
        botao_partida_local = Botao(partida_local_sprite_normal, partida_local_sprite_destacado, estados["partida_local"])
        self.botoes.append(botao_partida_local)

        historico_sprite_normal = Sprite("assets/imagem/tela_logado/botao_historico.png")
        historico_sprite_destacado = Sprite("assets/imagem/tela_logado/botao_historico_select.png")
        botao_historico = Botao(historico_sprite_normal, historico_sprite_destacado, estados["historico"])
        self.botoes.append(botao_historico)

        #substituir por botao de logout
        desconectar_sprite_normal = Sprite("assets/imagem/tela_logado/botao_desconectar.png")
        desconectar_sprite_destacado = Sprite("assets/imagem/tela_logado/botao_desconectar_select.png")
        botao_desconectar = Botao(desconectar_sprite_normal, desconectar_sprite_destacado, estados["desconectar"])
        self.botoes.append(botao_desconectar)

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
