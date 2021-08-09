from PPlay.gameimage import *


class Territorio:
    quantidade_tropas = 0
    cor_tropas = ""

    def __init__(self, name, img_path):
        self.name = name
        self.image = GameImage(img_path)

