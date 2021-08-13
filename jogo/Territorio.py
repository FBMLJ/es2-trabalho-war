from PPlay.gameimage import *
from constant import *
class Territorio:
    caminho_pasta_territorios = "assets/imagem/mapa/territorios/"

    def __init__(self, codigo):
        self.id = codigo
        self.nome = dicionario_territorios[self.id]
        self.img = GameImage(self.caminho_pasta_territorios + str(self.id) + ".png")
        self.img_select = GameImage(self.caminho_pasta_territorios + str(self.id)+"_select.png")
        self.selecionado = False
        self.vizinho = []
        self.quantidade_tropas = 0
        self.cor_tropas = None

    def set_cor_tropas(self, cor):
        self.cor_tropas = cor
        self.img = GameImage(self.caminho_pasta_territorios + dicionario_territorios[self.id] + "_" + cores[cor] + ".png")
