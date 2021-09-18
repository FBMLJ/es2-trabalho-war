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
        self.clicou_inicial = False
        self.clicou_vizinho = False
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
        
    
    def selecionar_territorio(self, mouse:Mouse, jogador:Player, etapa:int) -> None:
        if etapa > 1:
            return
        if mouse.is_button_pressed(1):
            self.clicou_inicial = True

        if self.clicou_inicial and not mouse.is_button_pressed(1):
            x, y = mouse.get_position()
            self.clicou_inicial = False
            self.colisao_mouse.set_position(x, y)
            self.colisao_mouse.draw()
            self.pode_desenhar = True
            for territorio in jogador.territorios:
                if self.colisao_mouse.collided_perfect(territorio.img):
                    #  durante a etapa de combate, nao posso selecionar um territorio atacante com um exercito
                    if(etapa == 2 and territorio.quantidade_tropas <= 1):
                        break
                    if len(self.territorios_selecionados) == 1:
                        self.limpa_territorios_selecionados()
                    territorio.selecionado = True
                    self.territorios_selecionados.append(territorio)
                    break

    def selecionar_inicial(self, mouse:Mouse, jogador:Player, etapa:int):
        if etapa < 2:
            return
        if mouse.is_button_pressed(1):
            self.clicou_inicial = True

        if self.clicou_inicial and not mouse.is_button_pressed(1):
            self.clicou_inicial = False
            x, y = mouse.get_position()
            self.colisao_mouse.set_position(x, y)
            self.colisao_mouse.draw()
            self.pode_desenhar = True
            for territorio in jogador.territorios:
                if self.colisao_mouse.collided_perfect(territorio.img):
                    #  durante a etapa de combate, nao posso selecionar um territorio atacante com um exercito
                    if (etapa == 2 and territorio.quantidade_tropas <= 1) or len(self.territorios_selecionados) > 0:
                        break
                    self.territorios_selecionados.append(territorio)

    def selecionar_vizinho(self, mouse:Mouse, jogador:Player, etapa:int): #  argumento 'etapa' indica em que etapa o turno esta
        if mouse.is_button_pressed(1) and len(self.territorios_selecionados) >= 1:
            self.clicou_vizinho = True

        if self.clicou_vizinho and not mouse.is_button_pressed(1):
            self.clicou_vizinho = False
            x, y = mouse.get_position()
            self.colisao_mouse.set_position(x, y)
            self.colisao_mouse.draw()
            self.pode_desenhar = True
            for territorio in self.lista_territorios:
                if (
                    self.colisao_mouse.collided_perfect(territorio.img) and 
                    territorio != self.territorios_selecionados[0] and
                    territorio.eh_vizinho(self.territorios_selecionados[0])
                   ):

                    if( 
                        (etapa == 2 and territorio.cor_tropas != self.territorios_selecionados[0].cor_tropas) or 
                        (etapa == 3 and territorio.cor_tropas == self.territorios_selecionados[0].cor_tropas)
                      ):
                        if len(self.territorios_selecionados) == 1:
                            territorio.selecionado = True
                            self.territorios_selecionados.append(territorio)
                        elif len(self.territorios_selecionados) == 2:
                            self.territorios_selecionados[1].selecionado = False
                            territorio.selecionado = True
                            self.territorios_selecionados[1] = territorio
                        #print("primario {} {}, secundario {} {}".format(self.territorios_selecionados[0].nome, self.territorios_selecionados[0].id, territorio.nome, territorio.id))
                        break #  Para nao percorrer toda a lista de territorios
                        
    def render(self, etapa):
        
        if (self.pode_desenhar):
            self.pode_desenhar = False
        
            self.fundo.draw()
            self.mapa.draw()
            for territorio in self.lista_territorios:
                territorio.img.draw()
            for territorio in self.lista_territorios:
                for territorio_selecionado in self.territorios_selecionados:
                    if (
                            territorio.eh_vizinho(self.territorios_selecionados[0]) and
                            ( 
                                (etapa == 2 and territorio.cor_tropas != self.territorios_selecionados[0].cor_tropas) or
                                (etapa == 3 and territorio.cor_tropas == self.territorios_selecionados[0].cor_tropas)
                            )
                        ):
                        territorio.img_highlight.draw()
                    if territorio_selecionado == territorio:
                        territorio.img_select.draw()

                self.desenha_quantidade_tropas(territorio)
                '''    
                tamanho_texto = 18
                cor_texto = (255,0,127)
                self.janela.draw_text(str(territorio.quantidade_tropas),
                    territorio.pos_texto_x, 
                    territorio.pos_texto_y, 
                    tamanho_texto, 
                    cor_texto
                    )
                '''
    def desenha_quantidade_tropas(self, territorio:Territorio):
        '''
        tamanho_texto = 28
        cor_texto = (255,255,255)
        self.janela.draw_text(
            str(territorio.quantidade_tropas),
            territorio.pos_texto_x-3, 
            territorio.pos_texto_y-3, 
            tamanho_texto, 
            cor_texto
            )
        '''
        tamanho_texto = 24
        #cor_texto = (255,0,127)
        #cor_texto = (255, 95, 31)
        cor_texto = (106,106,106)
        self.janela.draw_text(
            str(territorio.quantidade_tropas),
            territorio.pos_texto_x, 
            territorio.pos_texto_y, 
            tamanho_texto, 
            cor_texto,
            bold=True
            )
        

    def carrega_imagens_dos_territorios(self):

        for territorio in self.lista_territorios:
            territorio.carrega_imagem()

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
    
    def limpa_territorios_selecionados(self):
        for territorio in self.territorios_selecionados:
            territorio.selecionado = False
        self.territorios_selecionados = []

    def fim_de_turno(self,jogador:Player):
        for territorio in jogador.territorios:
            territorio.fim_de_turno()