from PPlay.window import Window
from PPlay.gameimage import GameImage
from PPlay.mouse import Mouse
from jogo.ControladorMapa import ControladorMapa
from jogo.MatchStarter import MatchStarter
from jogo.Objetivo import *
from jogo.Card import Card
from jogo.Player import Player
from jogo.CardManager import CardManager
from jogo.ObjectiveVerifier import ObjectiveVerifier
from jogo.TroopsManager import TroopsManager
from componentes.hudTurno import hudTurno
from constant import *

class ControladorPartida:
    caminho_hud = "assets/imagem/hud/"

    def __init__(self, janela:Window, jogadores: list):
        self.gerenciador_mapa = ControladorMapa(janela)
        self.gerenciador_cartas = CardManager()
        self.gerenciador_objetivos = ObjectiveVerifier()
        self.gerenciador_tropas = TroopsManager()
        self.jogadores = jogadores
        self.todos_os_objetivos = self.gerenciador_objetivos.gera_objetivos(self.gerenciador_mapa)
        self.iniciador_de_partida = MatchStarter()

        self.iniciador_de_partida.distribui_cores(self.jogadores)
        self.iniciador_de_partida.distribui_territorios(self.gerenciador_mapa.lista_territorios, self.jogadores)
        self.iniciador_de_partida.distribui_objetivos(self.todos_os_objetivos, self.jogadores)

        for i in jogadores:
            print(i.objetivo.descricao)
        for territorio in self.gerenciador_mapa.lista_territorios:
            print(territorio.cor_tropas)
            
        self.hud_turno = hudTurno(janela)
        self.janela = janela
        self.mouse = Mouse()
        self.jogador_vencedor = None
        self.baralho = []
        self.rodada = 1

    def loop(self):
        self.janela.clear()

        #game loop
        while self.jogador_vencedor == None:  #Condicional para checar se algum objetivo foi alcancado
            for jogador in self.jogadores:
                self.jogador_vencedor = self.gerenciador_objetivos.verifica_objetivos(self.jogadores, self.gerenciador_mapa.lista_territorios)
                if self.jogador_vencedor:
                    break
                '''
                Etapa 1 do turno: Distribuicao de exercitos
                '''
                self.gerenciador_tropas.recebimento_rodada(jogador, self.gerenciador_mapa.lista_continentes)  #Calcula
                etapa_1 = True
                while etapa_1:
                    nome_territorio_selecionado = self.gerenciador_mapa.selecionar_territorio(self.mouse)
                    
                if(self.rodada > 1): #Na primeira rodada so ha distribuicao de exercitos
                    
                    '''
                    Etapa 2 do turno: Combate
                    '''
                    etapa_2 = True
                    while etapa_2:
                        break
                    
                    '''
                    Etapa 3 do turno: Movimentacao de exercitos
                    '''
                    etapa_3 = True
                    while etapa_3:
                        break
                self.gerenciador_mapa.selecionar_territorio(self.mouse)
                self.render()
                self.janela.update()
            

    def render(self):
        self.gerenciador_mapa.render()
        self.hud_turno.render()

    def inicia_cartas(self) -> None:
        for id_territorio in dicionario_territorios:
            nome_territorio = dicionario_territorios[id_territorio]
            imagem = nome_territorio + "_carta.png"
            figura = dicionario_figura_territorio[id_territorio]
            self.todas_as_cartas.append(Card(nome_territorio, imagem, figura, False))