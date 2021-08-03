"""
Classe responsavel por, de acordo com o estado, gerar o menu correspondente
"""
from PPlay.window import *
from PPlay.gameimage import *


class Menu:
    def __init__(self, janela: Window, estado_do_jogo, usuario):

        self.usuario = usuario
        self.janela = janela
        self.estado_do_jogo = estado_do_jogo
    def inicia_menu(self):
        self.janela.set_title("WAR")
        self.fundo= GameImage()