from PPlay.mouse import Mouse
from PPlay.window import Window
from PPlay.gameimage import GameImage
from jogo.Territorio import *
from jogo.Continente import *
import constant

class ControladorMapa:

    caminho_img_mapa = "assets/imagem/mapa/"
    caminho_img_territorios = caminho_img_mapa+"territorios/"
    caminho_matriz_adjacencia = "jogo/matrizAdjacencia.txt"
    img_mapa = "mapa_war.png"
    img_fundo = "fundo.jpg"

    lista_territorios = []
    africa = None
    america_do_norte = None
    america_do_sul = None
    asia = None
    europa = None
    oceania = None

    dicionario_territorios = {
        1:"Congo",
        2:"Sudao",
        3:"Egito",
        4:"Madagascar",
        5:"Argelia",
        6:"Africa do Sul",
        7:"Alaska",
        8:"Alberta",
        9:"Mexico",
        10:"Nova Iorque",
        11:"Groenlandia",
        12:"Mackenzie",
        13:"Ottawa",
        14:"Labrador",
        15:"California",
        16:"Argentina",
        17:"Brasil",
        18:"Peru",
        19:"Venezuela",
        20:"Aral",
        21:"China",
        22:"India",
        23:"Tchita",
        24:"Japao",
        25:"Vladivostok",
        26:"Oriente Medio",
        27:"Mongolia",
        28:"Vietna",
        29:"Dudinka",
        30:"Omsk",
        31:"Siberia",
        32:"Reino Unido",
        33:"Islandia",
        34:"Alemanha",
        35:"Escandinavia",
        36:"Italia",
        37:"Moscou",
        38:"Franca",
        39:"Australia Oriental",
        40:"Sumatra",
        41:"Nova Guine",
        42:"Australia Ocidental"
    }

    def __init__(self, janela:Window):
        self.janela = janela
        self.fundo = GameImage(self.caminho_img_mapa+self.img_fundo)
        self.mapa = GameImage(self.caminho_img_mapa+self.img_mapa)
        self.inicia_territorios()
        self.inicia_continentes()

    def inicia_territorios(self):
        #Criando uma lista com todas as instancias de territorios
        for id_territorio in self.dicionario_territorios:
            nome_territorio = self.dicionario_territorios[id_territorio]
            self.lista_territorios.append(Territorio(nome_territorio, self.caminho_img_territorios + str(id_territorio)+".png"))
        
        #Criando lista de vizinhos de cada territorio
        arq = open(self.caminho_matriz_adjacencia,'r')
        linhas = arq.readlines()
        arq.close()
        matriz_adj = []
        for linha in linhas:
            matriz_adj.append(linha.split('\t'))

        for i in range(len(matriz_adj)):
            for j in range(len(matriz_adj[0])):
                if matriz_adj[i][j] == 1:
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
    
    def loop(self):
        self.janela.clear()
        mouse = Mouse()
        while True:
            self.render()
            self.janela.update()

    def render(self):
        self.fundo.draw()
        self.mapa.draw()
        for territorio in self.lista_territorios:
            territorio.img.draw()