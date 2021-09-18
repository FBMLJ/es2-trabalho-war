from pygame import transform
from PPlay.gameimage import *
from constant import *

class Territorio:
    caminho_pasta_territorios = "assets/imagem/mapa/territorios/"

    def __init__(self, codigo):
        self.id = codigo
        self.nome = dicionario_territorios[self.id]
        self.continente_nome = ""
        self.img = None
        self.img_select = None
        self.img_highlight = None #  Para realcar caso o territorio seja vizinho de um territorio atacante
        self.selecionado = False
        self.vizinho = []
        self.quantidade_tropas = 0
        self.tropas_deslocadas = 0
        self.cor_tropas = None
        #Variaveis para armazenar a posicao da quantidade de exercitos no territorio
        self.pos_texto_x = None
        self.pos_texto_y = None

    def __eq__(self, other) -> bool:
        return self.nome == other.nome

    def __ne__(self, other) -> bool:
        return self.nome != other.nome

    def perde_tropas(self, tropas_a_retirar: int) -> None:
        if self.quantidade_tropas >= tropas_a_retirar:
            self.quantidade_tropas -= tropas_a_retirar

    def recebe_tropas(self, tropas_a_receber: int) -> None:
        self.quantidade_tropas += tropas_a_receber

    def eh_vizinho(self, territorio_compr) -> bool:
        if territorio_compr in self.vizinho:
            return True
        else:
            return False

    def fim_de_turno(self):
        self.tropas_deslocadas = 0

    def set_cor_tropas(self, cor):
        self.cor_tropas = cor
        self.img = GameImage(self.caminho_pasta_territorios + str(self.id) + "_" + cores_traducao[cor] + ".png")
        self.muda_escala(int(PERCT_MAPA*LARGURA_PADRAO), int(PERCT_MAPA*ALTURA_PADRAO))
    
    def carrega_posicao_texto(self):
        self.pos_texto_x, self.pos_texto_y = dicionario_territorios_pos_texto[self.id]
    
    def muda_escala(self, nova_largura, nova_altura):
        self.img.image = transform.scale(self.img.image, (nova_largura, nova_altura))
        self.img_select.image = transform.scale(self.img_select.image, (nova_largura, nova_altura))
        self.img_highlight.image = transform.scale(self.img_highlight.image, (nova_largura, nova_altura))
        
    def carrega_imagem(self):
        caminho_img = self.caminho_pasta_territorios + str(self.id) + ".png"
        caminho_img_select = self.caminho_pasta_territorios + str(self.id)+"_select.png"
        caminho_img_highlight = self.caminho_pasta_territorios + str(self.id)+"_highlight.png"
        self.img = GameImage(caminho_img)
        self.img_select = GameImage(caminho_img_select)
        self.img_highlight = GameImage(caminho_img_highlight)

    def realcar_territorio(self):
        pass
    
    def desvanecer_territorio(self):
        pass
