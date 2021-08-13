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

        titulo = GameImage("assets/imagem/Login/email.png")
        self.loginCampo = CampoTexto(janela, titulo, janela.width/2 - 320, 240 ,640,60, 35)

        titulo = GameImage("assets/imagem/Login/senha.png")
        self.senhaCampo = CampoSenha(janela,titulo, janela.width/2 - 320, 380 ,640,60, 35)

        login_sprite = Sprite("assets/imagem/Login/botao_fazer_login.png")
        login_sprite_selecionado = Sprite("assets/imagem/Login/botao_fazer_login_select.png")
        self.botao_login = Botao(login_sprite, login_sprite_selecionado, estados["login"])
        self.botao_login.setposition(janela.width/2 - login_sprite.width/2, self.senhaCampo.y + self.senhaCampo.height + 50)
        
        self.barra_superior = GameImage("assets/imagem/barra_superior_geral.png")
        self.titulo_janela = GameImage("assets/imagem/Login/letrero_login.png")
        self.titulo_janela.set_position(50, self.barra_superior.height / 2 - self.titulo_janela.height / 2)

        sprite_x = Sprite("assets/imagem/historico/icon_x.png")
        self.botao_x = Botao(sprite_x, sprite_x, 20)
        self.botao_x.setposition(self.janela.width- self.botao_x.width-15, 15)
        

    def loop(self):

        self.janela.input_pygame = True

        clicou_login = False
        mouse = Mouse()

        while True:
            self.draw()

            saiu = self.botao_x.update()
            if saiu:
                self.janela.input_pygame = False
                return estados["menu_inicial"], None
            
            logar = self.botao_login.update()
            if logar:
                clicou_login = True

            if clicou_login and not mouse.is_button_pressed(1):
                sucesso, resultado = sign_in(self.loginCampo.texto, self.senhaCampo.texto)
                clicou_login = False
                if not sucesso:
                    print(resultado)
                else:
                    self.janela.input_pygame = False
                    print("Login feito com sucesso")
                    return estados["menu_logado"], resultado

            self.janela.update()

    def draw(self):
        super().draw()
        self.bg.draw()
        self.barra_superior.draw()
        self.titulo_janela.draw()
        self.botao_x.render()
        self.loginCampo.draw()
        #pygame.draw.rect(self.janela.get_screen(), (200,15,51),self.botao)
        self.senhaCampo.draw()
        self.botao_login.render()

    def evento(self, e):
        super().evento(e)
        self.loginCampo.evento(e)
        self.senhaCampo.evento(e)
