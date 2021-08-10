"""
Classe responsavel por gerenciar e instanciar as diversas telas do jogo
"""
from PPlay.window import *
from telas.Login import *
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

            if self.estado_do_jogo == estados["login"]:
                login = Login(self.janela)
                self.estado_do_jogo = login.loop()

            if self.estado_do_jogo == estados["sair"]:
                exit(0)