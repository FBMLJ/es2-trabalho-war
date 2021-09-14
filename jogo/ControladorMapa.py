from pygame import transform
from PPlay.mouse import Mouse
from PPlay.window import Window
from PPlay.gameimage import GameImage
from jogo.Territorio import *
from jogo.Continente import *
from constant import *

class ControladorMapa:

    caminho_img_mapa = "assets/imagem/mapa/"
    caminho_matriz_adjacencia = "jogo/matrizAdjacencia.txt"
    img_mapa = "mapa_war_conexoes.png"
    img_fundo = "fundo.jpg"
    img_colisao = "mouse_colisao.jpg"
    lista_territorios = [] #  Lista de todos os territorios do jogo
    #Instancias da classe Continentes
    africa = None
    america_do_norte = None
    america_do_sul = None
    asia = None
    europa = None
    oceania = None
    
    
    perct_mapa = 0.85 #  Variavel para diminuir o tamanho do mapa e continentes

    def __init__(self, janela:Window):
        self.pode_desenhar = True
        self.colisao_mouse = GameImage(self.caminho_img_mapa+self.img_colisao)
        self.janela = janela
        self.fundo = GameImage(self.caminho_img_mapa+self.img_fundo)
        self.mapa = GameImage(self.caminho_img_mapa+self.img_mapa)
        self.inicia_territorios()
        self.inicia_continentes()
        self.primeira_vez = True
        #Redimensionando as imagens, eh necessario usar .image pois eh classe do Pygame
        self.fundo.image = transform.scale(self.fundo.image, (janela.width, janela.height))
        self.mapa.image = transform.scale(self.mapa.image, (int(self.perct_mapa*LARGURA_PADRAO), int(self.perct_mapa*ALTURA_PADRAO)))
        for territorio in self.lista_territorios:
            territorio.img.image = transform.scale(territorio.img.image, (int(self.perct_mapa*LARGURA_PADRAO), int(self.perct_mapa*ALTURA_PADRAO)))
            territorio.img_select.image = transform.scale(territorio.img_select.image, (int(self.perct_mapa*LARGURA_PADRAO), int(self.perct_mapa*ALTURA_PADRAO)))
    def inicia_territorios(self):
        #Criando uma lista com todas as instancias de territorios
        for id_territorio in dicionario_territorios:
            self.lista_territorios.append(Territorio(id_territorio))
        
        #Criando lista de vizinhos de cada territorio
        arq = open(self.caminho_matriz_adjacencia,'r')
        linhas = arq.readlines()
        arq.close()
        matriz_adj = []
        for linha in linhas:
            matriz_adj.append(linha.strip('\n').split('\t'))
        for i in range(len(matriz_adj)):
            for j in range(len(matriz_adj[0])):
                if matriz_adj[i][j] == '1':
                    self.lista_territorios[i].vizinho.append( self.lista_territorios[j] )

    def inicia_continentes(self):
        #Listas de territorios por continentes para a criacao das instancias de continentes
        territorios_africa = []
        territorios_an = []
        territorios_as = []
        territorios_asia = []
        territorios_eu = []
        territorios_oc = []

        #Separando territorios por continentes, de acordo com seu id
        for i in range(len(self.lista_territorios)):
            if i+1 < 6:
                territorios_africa.append(self.lista_territorios[i])
            if i+1 > 6 and i+1 <= 15:
                territorios_an.append(self.lista_territorios[i])
            if i+1 > 16 and i+1 <= 19:
                territorios_as.append(self.lista_territorios[i])
            if i+1 > 19 and i+1 <=31:
                territorios_asia.append(self.lista_territorios[i])
            if i+1 > 31 and i+1 <= 38:
                territorios_eu.append(self.lista_territorios[i])
            if i+1 > 38 and i+1 <= 42:
                territorios_oc.append(self.lista_territorios[i])

        #Criando os continentes
        self.africa = Continente("Africa", territorios_africa, 3)
        self.america_do_norte = Continente("America do Norte", territorios_an, 5)
        self.america_do_sul = Continente("America do Sul", territorios_as, 2)
        self.asia = Continente("Asia", territorios_asia, 7)
        self.europa = Continente("Europa", territorios_eu, 5)
        self.oceania = Continente("Oceania", territorios_oc, 2)
    
    def selecionar_territorio(self, mouse:Mouse):
        x,y = mouse.get_position()
        self.colisao_mouse.set_position(x,y)
        territorio_selecionado = None
        if mouse.is_button_pressed(1):
            self.colisao_mouse.draw()
            self.pode_desenhar = True
            for territorio in self.lista_territorios:
                if self.colisao_mouse.collided_perfect(territorio.img):
                    territorio.selecionado = True
                    territorio_selecionado = territorio.nome
                elif territorio.selecionado: #  Caso o usuario tenha selecionado um novo territorio
                    territorio.selecionado = False
        return territorio_selecionado

    def render(self):
        
        if (self.pode_desenhar):
            self.pode_desenhar = False
        
            self.fundo.draw()
            self.mapa.draw()
            for territorio in self.lista_territorios:
                    territorio.img.draw()
                    if territorio.selecionado:
                        territorio.img_select.draw()
        