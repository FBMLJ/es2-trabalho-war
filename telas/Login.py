from telas.JanelaPadrao import JanelaPadrao
from PPlay.gameimage import GameImage
from PPlay.sprite import *
from PPlay.mouse import Mouse
from componentes.botao import *
from constant import estados
from componentes.campoTexto import CampoTexto
from componentes.campoSenha import CampoSenha
import pygame
from servico.Login import sign_in


"""botão provisorio preciso ser refeito com componente"""
class Login(JanelaPadrao):
    def __init__(self, janela):
        super().__init__(janela)
        self.bg = GameImage(image_file="./assets/imagem/tela_inicial/fundo.png")
        self.bg.set_scale(self.janela.width , self.janela.height)
        self.loginCampo = CampoTexto(janela, "Email:", janela.width/2 - 320, 240 ,640,60)
        self.senhaCampo = CampoSenha(janela,"Senha:", janela.width/2 - 320, 380 ,640,60)
        #self.botao = pygame.Rect([480,490,320,60])
        login_sprite = Sprite("assets/imagem/tela_inicial/botao_login.png")
        login_sprite_selecionado = Sprite("assets/imagem/tela_inicial/botao_login_select.png")
        self.botao_login = Botao(login_sprite, login_sprite_selecionado, estados["login"])
        self.botao_login.setposition(janela.width/2 - login_sprite.width/2, self.senhaCampo.y + self.senhaCampo.height + 50)
        
        self.barra_superior = GameImage("assets/imagem/historico/barra.jpg")

        sprite_x = Sprite("assets/imagem/historico/icon_x.png")
        self.botao_x = Botao(sprite_x, sprite_x, 20)
        self.botao_x.setposition(self.janela.width- self.botao_x.width-15, 15)
        

    def loop(self):

        self.janela.input_pygame = True

        while True:
            self.draw()

            saiu = self.botao_x.update()
            if saiu:
                self.janela.input_pygame = False
                return estados["menu_inicial"]
            
            logar = self.botao_login.update()
            if logar:
                token = sign_in(self.loginCampo.texto, self.senhaCampo.texto)
                if not token:
                    print("Falha ao fazer o login")
                else:
                    self.janela.input_pygame = False
                    return estados["menu_logado"]
                    print("Login feito com sucesso")
                
            self.janela.update()

    def draw(self):
        super().draw()
        self.bg.draw()
        self.barra_superior.draw()
        self.botao_x.render()
        self.loginCampo.draw()
        #pygame.draw.rect(self.janela.get_screen(), (200,15,51),self.botao)
        self.senhaCampo.draw()
        self.botao_login.render()

    def evento(self, e):
        super().evento(e)
        """
        if e.type == pygame.MOUSEBUTTONDOWN and self.botao.collidepoint(Mouse().get_position()):
            token = sign_in(self.loginCampo.texto, self.senhaCampo.texto)
            if not token:
                print("Falha ao fazer o login")
            else:
                self.login_sucesso = True
                print("Login feito com sucesso")
        """
        self.loginCampo.evento(e)
        self.senhaCampo.evento(e)
