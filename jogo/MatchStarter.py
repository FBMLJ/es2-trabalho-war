from random import shuffle
from jogo.Objetivo import Objetivo
from jogo.ObjectiveVerifier import ObjectiveVerifier
from jogo.Player import Player

from constant import *

class MatchStarter:
    '''
    Classe responsavel por iniciar o jogo
    Distribui cartas, territorios e objetivos
    '''
    def __init__(self) -> None:
        self.verificador_objetivos = ObjectiveVerifier()

    '''
    Funcoes para embaralhar listas de cartas, territorios, objetivos e jogadores
    '''
    def embaralha_cartas(self, cartas: list) -> None:
        shuffle(cartas)

    def embaralha_territorios(self, territorios: list) -> None:
        shuffle(territorios)
    
    def embaralha_objetivos(self, objetivos: list) -> None:
        shuffle(objetivos)

    def embaralha_jogadores(self, jogadores: list) -> None:
        shuffle(jogadores)

    '''
    Funcao para distribuir territorios para cada jogador
    Primeiro embaralha os territorios e a ordem dos jogadores
    Depois da os territorios ciclicamente para cada jogador
    '''
    def distribui_territorios(self, territorios: list, jogadores: list) -> None:
        #Primeiro embaralha os territorios e a ordem dos jogadores
        self.embaralha_territorios(territorios)
        self.embaralha_jogadores(jogadores)
        #Depois da os territorios ciclicamente para cada jogador
        num_de_jogadores = len(jogadores)
        jogador_a_receber_territorio = 0
        for i in range(len(territorios)):
            jogadores[jogador_a_receber_territorio].territorios.append(territorios[i])
            territorios[i].cor_tropas = jogadores[jogador_a_receber_territorio].cor
            territorios[i].quantidade_tropas = 1
            if jogador_a_receber_territorio < num_de_jogadores - 1:
                jogador_a_receber_territorio += 1
            else:
                jogador_a_receber_territorio = 0

    '''
    Funcao que distribui objetivos
    Primeiro embaralha a ordem dos jogadores
    Depois Filtra os objetivos para que objetivos impossiveis nao possam ser sorteados
    Depois Sorteia um objetivo para cada jogador
    Jogador nao pode ter o objetivo de destruir a si mesmo, se isso acontecer sorteia de novo o objetivo
    '''
    def distribui_objetivos(self, objetivos: list, jogadores: list) -> None:
        #Primeiro embaralha a ordem dos jogadores
        self.embaralha_jogadores(jogadores)
        #Depois Filtra os objetivos para que objetivos impossiveis nao possam ser sorteados
        objetivos_filtrados = self.verificador_objetivos.filtrar(objetivos, jogadores)
        #Depois Sorteia um objetivo para cada jogador
        for jogador in jogadores:
            buscando_objetivo = True
            while(buscando_objetivo):
                self.sorteia_objetivo(jogador, objetivos_filtrados)
                #Jogador nao pode ter o objetivo de destruir a si mesmo, se isso acontecer sorteia de novo o objetivo
                if jogador.objetivo.cor_a_destruir != jogador.cor:
                    buscando_objetivo = False
                    objetivos_filtrados.remove(jogador.objetivo)

    '''
    Funcao que sorteia um cores para os jogadores
    primeiro embaralha os jogadores
    depois passa uma cor para cada um
    '''
    def distribui_cores(self, jogadores):
        self.embaralha_jogadores(jogadores)
        indice = 0
        for cor in cores:
            if indice > len(jogadores) - 1:
                break
            jogadores[indice].cor = cor
            indice += 1

    '''
    Funcao que sorteia um objetivo para um jogador
    Primeiro embaralha a lista de objetivos
    Depois tira o primeiro objetivo para o jogador
    '''
    def sorteia_objetivo(self, jogador: Player, objetivos: list) -> None:
        self.embaralha_objetivos(objetivos)
        jogador.objetivo = objetivos[0]
