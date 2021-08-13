from PPlay.window import Window
from PPlay.gameimage import GameImage
from PPlay.mouse import Mouse
from jogo.ControladorMapa import ControladorMapa
from componentes.hudTurno import hudTurno
from constant import *

class ControladorPartida:
    caminho_hud = "assets/imagem/hud/"

    def __init__(self, janela:Window):
        self.controlador_mapa = ControladorMapa(janela)
        self.hud_turno = hudTurno(janela)
        self.janela = janela
        self.mouse = Mouse()

    def loop(self):
        self.janela.clear()
        while True:
            self.controlador_mapa.selecionar_territorio(self.mouse)
            self.render()
            self.janela.update()

    def render(self):
        self.controlador_mapa.render()
        self.hud_turno.render()