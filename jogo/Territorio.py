from ..PPlay.gameimage import *

class Territorio:

    quantidade_tropas = 0
    cor_tropas = None
    vizinho = []
    
    def __init__(self, nome, caminho_img):
        self.nome = nome
        self.img = GameImage(caminho_img)

