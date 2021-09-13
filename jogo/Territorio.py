from PPlay.gameimage import *
from constant import *
class Territorio:
    caminho_pasta_territorios = "assets/imagem/mapa/territorios/"

    def __init__(self, codigo):
        self.id = codigo
        self.nome = dicionario_territorios[self.id]
        self.continente_nome = ""
        self.img = GameImage(self.caminho_pasta_territorios + str(self.id) + ".png")
        self.img_select = GameImage(self.caminho_pasta_territorios + str(self.id)+"_select.png")
        self.selecionado = False
        self.vizinho = []
        self.quantidade_tropas = 0
        self.tropas_deslocadas = 0
        self.cor_tropas = None

    def __eq__(self, other):
        return self.nome == other.nome

    def perde_tropas(self, tropas_a_retirar: int) -> None:
        if self.quantidade_tropas >= tropas_a_retirar:
            self.quantidade_tropas -= tropas_a_retirar

    def recebe_tropas(self, tropas_a_receber: int) -> None:
        self.quantidade_tropas += tropas_a_receber

    def esta_na_fronteira(self, territorio_compr) -> bool:
        if territorio_compr in self.vizinho:
            return True
        else:
            return False

    def fim_de_turno(self):
        self.tropas_deslocadas = 0

    def set_cor_tropas(self, cor):
        self.cor_tropas = cor
        self.img = GameImage(self.caminho_pasta_territorios + dicionario_territorios[self.id] + "_" + cores[cor] + ".png")
