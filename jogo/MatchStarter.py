from PPlay.gameimage import GameImage
from random import shuffle
from jogo.Territorio import Territorio
from jogo.Objetivo import Objetivo
from jogo.ObjectiveVerifier import ObjectiveVerifier
from jogo.Player import Player
from jogo.Continente import Continente
import os

from constant import *

class MatchStarter:
    '''
    Classe responsavel por iniciar o jogo
    Distribui cartas, territorios e objetivos
    '''
    def __init__(self) -> None:

        self.caminho_matriz_adjacencia = "matrizAdjacencia.txt"

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


    def inicia_territorios(self) -> list:

        lista_territorios = []

        #Criando uma lista com todas as instancias de territorios
        index = 0
        for id_territorio in dicionario_territorios:
            lista_territorios.append(Territorio(id_territorio))
            lista_territorios[index].carrega_posicao_texto()
            index += 1

        #Criando lista de vizinhos de cada territorio
        arq = open(os.path.dirname(os.path.abspath(__file__))+"/"+self.caminho_matriz_adjacencia,'r')
        linhas = arq.readlines()
        arq.close()
        matriz_adj = []
        for linha in linhas:
            matriz_adj.append(linha.strip('\n').split('\t'))
        for i in range(len(matriz_adj)):
            for j in range(len(matriz_adj[0])):
                if matriz_adj[i][j] == '1':
                    lista_territorios[i].vizinho.append(lista_territorios[j])
        
        return lista_territorios

    def inicia_continentes(self, lista_territorios):

        #Listas de territorios por continentes para a criacao das instancias de continentes
        territorios_africa = []
        territorios_an = []
        territorios_as = []
        territorios_asia = []
        territorios_eu = []
        territorios_oc = []

        #Separando territorios por continentes, de acordo com seu id
        for i in range(len(lista_territorios)):
            if i+1 < 6:
                lista_territorios[i].continente_nome = "Africa"
                territorios_africa.append(lista_territorios[i])
            if i+1 > 6 and i+1 <= 15:
                lista_territorios[i].continente_nome = "America do Norte"
                territorios_an.append(lista_territorios[i])
            if i+1 > 16 and i+1 <= 19:
                lista_territorios[i].continente_nome = "America do Sul"
                territorios_as.append(lista_territorios[i])
            if i+1 > 19 and i+1 <=31:
                lista_territorios[i].continente_nome = "Asia"
                territorios_asia.append(lista_territorios[i])
            if i+1 > 31 and i+1 <= 38:
                lista_territorios[i].continente_nome = "Europa"
                territorios_eu.append(lista_territorios[i])
            if i+1 > 38 and i+1 <= 42:
                lista_territorios[i].continente_nome = "Oceania"
                territorios_oc.append(lista_territorios[i])

        #Criando os continentes
        africa = Continente("Africa", territorios_africa, 3)
        america_do_norte = Continente("America do Norte", territorios_an, 5)
        america_do_sul = Continente("America do Sul", territorios_as, 2)
        asia = Continente("Asia", territorios_asia, 7)
        europa = Continente("Europa", territorios_eu, 5)
        oceania = Continente("Oceania", territorios_oc, 2)
        lista_continentes = [
            africa, america_do_norte, america_do_sul,    
            asia, europa, oceania
            ]
        return lista_continentes

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
            cor_atual = jogadores[jogador_a_receber_territorio].cor
            territorios[i].set_cor_tropas(cor_atual)
            territorios[i].quantidade_tropas = 1
            #condicional para fazer o ciclo entre os jogadores
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
