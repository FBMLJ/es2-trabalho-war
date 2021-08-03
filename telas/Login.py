from telas.JanelaPadrao import JanelaPadrao
from PPlay.sprite import Sprite
class Login(JanelaPadrao):
    def __init__(self, janela):
        super().__init__(janela)
        self.bg = Sprite(image_file="./assets/imagem/tela_inicial/Credit-Marines-Flickr-CC-BY-NC-2.png")
        

    def draw(self):
        return super().draw()
        self.bg.draw()