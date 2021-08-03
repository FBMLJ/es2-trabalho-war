from telas.JanelaPadrao import JanelaPadrao
from PPlay.gameimage import GameImage
class Login(JanelaPadrao):
    def __init__(self, janela):
        super().__init__(janela)
        self.bg = GameImage(image_file="./assets/imagem/tela_inicial/Credit-Marines-Flickr-CC-BY-NC-2.png")
        self.bg.set_scale(self.janela.width , self.janela.height)
        

    def draw(self):
        super().draw()
        self.bg.draw()