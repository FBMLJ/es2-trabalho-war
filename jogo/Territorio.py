from PPlay.gameimage import *

class Territorio:
    
    def __init__(self, nome, caminho_img):
        self.nome = nome
        self.img = GameImage(caminho_img)
        self.vizinho = []
        self.quantidade_tropas = 0
        self.cor_tropas = None
