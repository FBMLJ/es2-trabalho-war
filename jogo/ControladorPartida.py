from PPlay.window import Window
from PPlay.gameimage import GameImage
from PPlay.mouse import Mouse
from jogo.ControladorMapa import ControladorMapa
from jogo.MatchStarter import MatchStarter
from jogo.Card import Card
from jogo.Player import Player
from jogo.CardManager import CardManager
from jogo.ObjectiveVerifier import ObjectiveVerifier
from jogo.TroopsManager import TroopsManager
from componentes.hudTurno import hudTurno
from constant import *

class ControladorPartida:
    caminho_hud = "assets/imagem/hud/"

    def __init__(self, janela:Window, jogadores:list):
        self.controlador_mapa = ControladorMapa(janela)
        self.iniciador_partida = MatchStarter(jogadores)
        self.gerenciador_cartas = CardManager()
        self.gerenciador_objetivos = ObjectiveVerifier()
        self.gerenciador_tropas = TroopsManager()
        self.hud_turno = hudTurno(janela)
        self.janela = janela
        self.mouse = Mouse()
        self.jogadores = jogadores
        self.jogador_vencedor = None
        self.baralho = []
        self.rodada = 1

    def loop(self):
        self.janela.clear()
        
        #Inicializacao do jogo: distribuir os territorios e objetivos para todos os jogadores
        self.baralho = self.gerenciador_cartas.inicia_cartas()
        self.iniciador_partida.distribui_territorios(self.controlador_mapa.lista_territorios, self.jogadores)
        for jogador in self.jogadores:
            self.gerenciador_tropas.recebimento_inicial(jogador)  #Colocando um exercito em cada territorio do jogador
        self.iniciador_partida.distribui_objetivos()

        #game loop
        while self.jogador_vencedor == None:  #Condicional para checar se algum objetivo foi alcancado
            for jogador in self.jogadores:
                self.jogador_vencedor = self.gerenciador_objetivos(self.jogadores, self.controlador_mapa.lista_territorios)
                if self.jogador_vencedor:
                    break
                '''
                Etapa 1 do turno: Distribuicao de exercitos
                '''
                
                '''
                Etapa 2 do turno: Combate
                '''
                if(self.rodada > 1): #Na primeira rodada nenhum jogador pode atacar
                    break
                '''
                Etapa 3 do turno: Movimentacao de exercitos
                '''
                self.controlador_mapa.selecionar_territorio(self.mouse)
                self.render()
                self.janela.update()
            

    def render(self):
        self.controlador_mapa.render()
        self.hud_turno.render()