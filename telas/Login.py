from telas.JanelaPadrao import JanelaPadrao
from PPlay.gameimage import GameImage
from componentes.campoTexto import CampoTexto
import pygame
class Login(JanelaPadrao):
    def __init__(self, janela):
        super().__init__(janela)
        self.bg = GameImage(image_file="./assets/imagem/tela_inicial/Credit-Marines-Flickr-CC-BY-NC-2.png")
        self.bg.set_scale(self.janela.width , self.janela.height)
        self.loginCampo = CampoTexto(janela,30, 30 ,40,10)
        
        

    def draw(self):
        super().draw()
        self.bg.draw()
        self.loginCampo.draw()

    def evento(self, e):
        super().evento(e)

        self.loginCampo.evento(e)
