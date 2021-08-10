"""
Classe responsavel por gerenciar e instanciar as diversas telas do jogo
"""
from PPlay.window import *
from telas.HistoricoDePartidas import *
from telas.Login import *
from telas.MenuLogado import *
from telas.MenuInicial import *
from constant import estados


class ControladorJogo:

    def __init__(self, janela):
        self.janela = janela
        self.estado_do_jogo = estados["menu_inicial"]

    def iniciar_jogo(self):

        while True:

            if self.estado_do_jogo == estados["menu_inicial"]:
                menu_inicial = MenuInicial(self.janela)
                self.estado_do_jogo = menu_inicial.loop()

            elif self.estado_do_jogo == estados["login"]:
                login = Login(self.janela)
                self.estado_do_jogo = login.loop()

            elif self.estado_do_jogo == estados["menu_logado"]:
                menu_logado = MenuLogado(self.janela)
                self.estado_do_jogo = menu_logado.loop()

            elif self.estado_do_jogo == estados["historico"]:
                historico = HistoricoDePartidas(self.janela, "id2")
                self.estado_do_jogo = historico.loop()

            elif self.estado_do_jogo == estados["sair"]:
                exit(0)

            else:
                exit(0)
