from telas.JanelaPadrao import JanelaPadrao
from PPlay.gameimage import GameImage
from PPlay.mouse import Mouse
from constant import estados
from componentes.campoTexto import CampoTexto
from componentes.campoSenha import CampoSenha
import pygame
from servico.Login import sign_in


"""botão provisorio preciso ser refeito com componente"""
class Login(JanelaPadrao):
    def __init__(self, janela):
        super().__init__(janela)
        self.login_sucesso = False
        self.bg = GameImage(image_file="./assets/imagem/tela_inicial/fundo.png")
        self.bg.set_scale(self.janela.width , self.janela.height)
        self.loginCampo = CampoTexto(janela, "Email:", 320, 240 ,640,60)
        self.senhaCampo = CampoSenha(janela,"Senha:", 320, 380 ,640,60)
        self.botao = pygame.Rect([480,490,320,60])
        

    def loop(self):

        self.janela.input_pygame = True

        while True:
            self.draw()
            if self.login_sucesso:
                self.janela.input_pygame = False
                return estados["menu_logado"]
            self.janela.update()

    def draw(self):
        super().draw()
        self.bg.draw()
        self.loginCampo.draw()
        pygame.draw.rect(self.janela.get_screen(), (200,15,51),self.botao)
        self.senhaCampo.draw()

    def evento(self, e):
        super().evento(e)
        if e.type == pygame.MOUSEBUTTONDOWN and self.botao.collidepoint(Mouse().get_position()):
            token = sign_in(self.loginCampo.texto, self.senhaCampo.texto)
            if not token:
                print("Falha ao fazer o login")
            else:
                self.login_sucesso = True
                print("Login feito com sucesso")
        self.loginCampo.evento(e)
        self.senhaCampo.evento(e)
