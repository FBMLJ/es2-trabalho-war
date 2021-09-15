from jogo.Player import Player
from pygame import transform
from PPlay.mouse import Mouse
from PPlay.window import Window
from PPlay.gameimage import GameImage
from jogo.Territorio import Territorio
from jogo.Continente import Continente
from constant import *

class ControladorMapa:

    caminho_img_mapa = "assets/imagem/mapa/"
    img_mapa = "mapa_war_conexoes.png"
    img_fundo = "fundo.jpg"
    img_colisao = "mouse_colisao.jpg"
    lista_territorios = [] #  Lista de todos os territorios do jogo
    lista_continentes = []
    #Instancias da classe Continentes
    africa = None
    america_do_norte = None
    america_do_sul = None
    asia = None
    europa = None
    oceania = None
    territorios_selecionados = [] #  primeira posicao armazenara o territorio que recebera tropa na etapa 1,
                                  #  atacante na etapa 2, ou territorio que tera sua tropa movida na etapa 3
                                  #  a segunda posicao armazenara o territorio desensor na etapa 2 ou o territorio que recebera tropa
                                  #  movida de outro territorio na etapa 3

    def __init__(self, janela: Window):
        self.pode_desenhar = True
        self.colisao_mouse = GameImage(self.caminho_img_mapa+self.img_colisao)
        self.janela = janela
        self.fundo = GameImage(self.caminho_img_mapa+self.img_fundo)
        self.mapa = GameImage(self.caminho_img_mapa+self.img_mapa)
        #self.inicia_territorios()
        #self.inicia_continentes()
        self.primeira_vez = True
        #Redimensionando as imagens, eh necessario usar .image pois eh classe do Pygame
        self.fundo.image = transform.scale(self.fundo.image, (janela.width, janela.height))
        self.mapa.image = transform.scale(self.mapa.image, (int(PERCT_MAPA*LARGURA_PADRAO), int(PERCT_MAPA*ALTURA_PADRAO)))
        for territorio in self.lista_territorios:
            territorio.muda_escala(int(PERCT_MAPA*LARGURA_PADRAO), int(PERCT_MAPA*ALTURA_PADRAO))
            #territorio.img.image = transform.scale(territorio.img.image, (int(PERCT_MAPA*LARGURA_PADRAO), int(PERCT_MAPA*ALTURA_PADRAO)))
            #territorio.img_select.image = transform.scale(territorio.img_select.image, (int(PERCT_MAPA*LARGURA_PADRAO), int(PERCT_MAPA*ALTURA_PADRAO)))
        
    
    def selecionar_territorio(self, mouse:Mouse, jogador:Player,etapa:int) -> None:
        x,y = mouse.get_position()
        self.colisao_mouse.set_position(x,y)
        if mouse.is_button_pressed(1):
            self.colisao_mouse.draw()
            self.pode_desenhar = True
            for territorio in self.lista_territorios:
                if self.colisao_mouse.collided_perfect(territorio.img):
                    if(etapa == 1 and territorio.cor_tropas == jogador.cor):
                        if len(self.territorios_selecionados) == 1:
                            self.territorios_selecionados[0] = territorio
                        elif len(self.territorios_selecionados) == 0:
                            self.territorios_selecionados.append(territorio)
                    if(etapa == 2):
                        if len(self.territorios_selecionados) == 0 and territorio.cor_tropas == jogador.cor:
                            self.territorios_selecionados.append(territorio) #  nenhum territorio foi selecionado, logo, esse sera o atacante
                        elif len(self.territorios_selecionados) == 1:
                            pass
                    #print("{}:({},{})".format(territorio.id, x, y))

    def render(self):
        
        if (self.pode_desenhar):
            self.pode_desenhar = False
        
            self.fundo.draw()
            self.mapa.draw()
            for territorio in self.lista_territorios:
                territorio.img.draw()
            for territorio in self.lista_territorios:
                for territorio_selecionado in self.territorios_selecionados:
                    if territorio_selecionado.nome == territorio.nome:
                        territorio.img_select.draw()
                tamanho_texto = 18
                cor_texto = (255,0,127)
                self.janela.draw_text(str(territorio.quantidade_tropas),
                    territorio.pos_texto_x, 
                    territorio.pos_texto_y, 
                    tamanho_texto, 
                    cor_texto
                    )
    
    def set_lista_continentes(self, lista_continentes):

        for continente in lista_continentes:
            
            if continente.nome == "Africa":
                self.africa = continente
            elif continente.nome == "America do Norte":
                self.america_do_norte = continente
            elif continente.nome == "America do Sul":
                self.america_do_sul = continente
            elif continente.nome == "Asia":
                self.asia = continente
            elif continente.nome == "Europa":
                self.europa = continente
            elif continente.nome == "Oceania":
                self.oceania = continente
        
        self.lista_continentes = lista_continentes