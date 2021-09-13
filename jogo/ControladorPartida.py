from PPlay.window import Window
from PPlay.gameimage import GameImage
from PPlay.mouse import Mouse
from jogo.ControladorMapa import ControladorMapa
from jogo.MatchStarter import MatchStarter
from jogo.Card import Card
from componentes.hudTurno import hudTurno
from constant import *

class ControladorPartida:
    caminho_hud = "assets/imagem/hud/"

    def __init__(self, janela:Window):
        self.controlador_mapa = ControladorMapa(janela)
        self.iniciador_de_partida = MatchStarter()
        self.hud_turno = hudTurno(janela)
        self.janela = janela
        self.mouse = Mouse()
        self.todas_as_cartas = [
            # Coringas
            Card(None, "coringa_carta.png", None, True),
            Card(None, "coringa_carta.png", None, True)
        ]

    def loop(self):
        self.janela.clear()
        while True:
            self.controlador_mapa.selecionar_territorio(self.mouse)
            self.render()
            self.janela.update()

    def render(self):
        self.controlador_mapa.render()
        self.hud_turno.render()

    def inicia_cartas(self) -> None:
        for id_territorio in dicionario_territorios:
            nome_territorio = dicionario_territorios[id_territorio]
            imagem = nome_territorio + "_carta.png"
            figura = dicionario_figura_territorio[id_territorio]
            self.todas_as_cartas.append(Card(nome_territorio, imagem, figura, False))