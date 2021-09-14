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
        self.controlador_mapa = ControladorMapa(janela)
        self.jogadores = jogadores
        self.todos_os_objetivos = self.gera_objetivos()
        self.iniciador_de_partida = MatchStarter()
        self.iniciador_de_partida.distribui_cores(self.jogadores)
        self.iniciador_de_partida.distribui_territorios(self.controlador_mapa.lista_territorios, self.jogadores)
        self.iniciador_de_partida.distribui_objetivos(self.todos_os_objetivos, self.jogadores)
        for i in jogadores:
            print(i.objetivo.descricao)
        for territorio in self.controlador_mapa.lista_territorios:
            print(territorio.cor_tropas)
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

    def inicia_cartas(self) -> None:
        for id_territorio in dicionario_territorios:
            nome_territorio = dicionario_territorios[id_territorio]
            imagem = nome_territorio + "_carta.png"
            figura = dicionario_figura_territorio[id_territorio]
            self.todas_as_cartas.append(Card(nome_territorio, imagem, figura, False))

    '''
    Funcao que gera todos os objetivos possíveis do jogo 
    e os armazena em uma lista para que possam ser distribuidos
    '''
    def gera_objetivos(self):

        lista_de_objetivos = []

        # adiciona todos os objetivos de destruir cores
        for cor in cores:
            objetivo_atual = Objetivo()
            objetivo_atual.descricao = "Destruir a cor " + cor
            objetivo_atual.cor_a_destruir = cor
            lista_de_objetivos.append(objetivo_atual)

        # adiciona o objetivo de conquistar Europa + américa do sul
        objetivo_atual = Objetivo()
        objetivo_atual.descricao = "Conquistar a Europa e a América do Sul"
        objetivo_atual.continentes_a_conquistar.append(self.controlador_mapa.europa)
        objetivo_atual.continentes_a_conquistar.append(self.controlador_mapa.america_do_sul)
        lista_de_objetivos.append(objetivo_atual)

        # adiciona o objetivo de conquistar Oceania + Ásia
        objetivo_atual = Objetivo()
        objetivo_atual.descricao = "Conquistar a Oceania e a Ásia"
        objetivo_atual.continentes_a_conquistar.append(self.controlador_mapa.oceania)
        objetivo_atual.continentes_a_conquistar.append(self.controlador_mapa.asia)
        lista_de_objetivos.append(objetivo_atual)

        # adiciona o objetivo de conquistar América do Norte e África
        objetivo_atual = Objetivo()
        objetivo_atual.descricao = "Conquistar a América do Norte e a África"
        objetivo_atual.continentes_a_conquistar.append(self.controlador_mapa.america_do_norte)
        objetivo_atual.continentes_a_conquistar.append(self.controlador_mapa.africa)
        lista_de_objetivos.append(objetivo_atual)

        # adiciona o objetivo de conquistar América do Norte e Oceania
        objetivo_atual = Objetivo()
        objetivo_atual.descricao = "Conquistar a América do Norte e a Oceania"
        objetivo_atual.continentes_a_conquistar.append(self.controlador_mapa.america_do_norte)
        objetivo_atual.continentes_a_conquistar.append(self.controlador_mapa.oceania)
        lista_de_objetivos.append(objetivo_atual)

        # adiciona o objetivo de conquistar Ásia e América do Sul
        objetivo_atual = Objetivo()
        objetivo_atual.descricao = "Conquistar a Ásia e a América do Sul"
        objetivo_atual.continentes_a_conquistar.append(self.controlador_mapa.asia)
        objetivo_atual.continentes_a_conquistar.append(self.controlador_mapa.america_do_sul)
        lista_de_objetivos.append(objetivo_atual)

        # adiciona o objetivo de conquistar Ásia e África
        objetivo_atual = Objetivo()
        objetivo_atual.descricao = "Conquistar a Ásia e a África"
        objetivo_atual.continentes_a_conquistar.append(self.controlador_mapa.asia)
        objetivo_atual.continentes_a_conquistar.append(self.controlador_mapa.africa)
        lista_de_objetivos.append(objetivo_atual)

        # adiciona o objetivo de conquistar 18 territórios com no mínimo duas tropas em cada
        objetivo_atual = Objetivo()
        objetivo_atual.descricao = "Conquistar 18 Territórios com no mínimo 2 tropas em cada"
        objetivo_atual.territorios_a_conquistar_qtd = 18
        objetivo_atual.tropas_em_cada_territorios = 2
        lista_de_objetivos.append(objetivo_atual)

        # adiciona o objetivo de conquistar 24 territórios
        objetivo_atual = Objetivo()
        objetivo_atual.descricao = "Conquistar 24 Territórios"
        objetivo_atual.territorios_a_conquistar_qtd = 24
        lista_de_objetivos.append(objetivo_atual)

        return lista_de_objetivos
