"""
Classe responsavel por gerenciar e instanciar as diversas telas do jogo
"""
from PPlay.window import *
import constant

class ControladorJogo:

    estado_do_jogo = 1 # Depois desenvolveremos mais esse atributo

    def __init__(self):
        self.janela = Window(constant.LARGURA_PADRAO, constant.ALTURA_PADRAO)

    def iniciar_jogo(self):
        pass