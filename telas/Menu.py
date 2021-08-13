"""
Classe responsavel por, de acordo com o estado, gerar o menu correspondente
"""
from PPlay.window import *
from telas import(
    ControladorJogo,
    MenuLogin,
    MenuInicial
    )


class Menu:
    def __init__(self, janela: Window, usuario):

        self.usuario = usuario
        self.janela = janela

    def inicia_menu(self):
        if ControladorJogo.estado_do_jogo == 1:
            menu_inicial = MenuInicial(self.janela)
            ControladorJogo.estado_do_jogo=menu_inicial.loop()
        if ControladorJogo.estado_do_jogo==2:
            menu_login = MenuLogin(self.janela)