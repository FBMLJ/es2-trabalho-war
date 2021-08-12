from telas.JanelaPadrao import JanelaPadrao
from PPlay.gameimage import GameImage
from PPlay.sprite import *
from componentes.botao import *
from  PPlay.mouse import Mouse
from componentes.campoTexto import CampoTexto
from componentes.campoSenha import CampoSenha
import pygame
from servico.Login import cadastro
from constant import *

"""botão provisorio preciso ser refeito com componente"""
class Cadastro(JanelaPadrao):
    def __init__(self, janela):
        super().__init__(janela)
        self.bg = GameImage(image_file="./assets/imagem/tela_inicial/fundo.png")
        self.bg.set_scale(self.janela.width , self.janela.height)
        self.loginCampo = CampoTexto(janela,"Informe seu Email:", janela.width/2 - 320, 180 , 640,60)
        self.usernameCampo = CampoTexto(janela, "Informe um nome de usuário:", janela.width/2 - 320, 280, 640, 60)
        self.senhaCampo = CampoSenha(janela, "Defina uma senha:", janela.width/2 - 320, 380 , 640,60)
        self.confirmaSenhaCampo = CampoSenha(janela,"Confirme a senha:", janela.width/2 - 320, 480 ,640,60)
        botao_sprite = Sprite("assets/imagem/tela_inicial/botao_login.png")
        botao_selecionado_sprite = Sprite("assets/imagem/tela_inicial/botao_login_select.png")
        self.botao = Botao(botao_sprite, botao_selecionado_sprite, estados["cadastro"])
        altura_botao = self.confirmaSenhaCampo.y + self.confirmaSenhaCampo.height + 25
        self.botao.setposition(self.janela.width/2 - self.botao.width/2, altura_botao)
        #self.botao = pygame.Rect([480,490,320,60])

        self.barra_superior = GameImage("assets/imagem/historico/barra.jpg")

        sprite_x = Sprite("assets/imagem/historico/icon_x.png")
        self.botao_x = Botao(sprite_x, sprite_x, 20)
        self.botao_x.setposition(self.janela.width- self.botao_x.width-15, 15)
        

    def loop(self):

        self.janela.input_pygame = True

        clicou_cadastro = False
        mouse = Mouse()

        while True:

            self.draw()

            saiu = self.botao_x.update()
            if saiu:
                self.janela.input_pygame = False
                return estados["menu_inicial"], None

            cadastrar = self.botao.update()
            if cadastrar:
                clicou_cadastro = True

            if clicou_cadastro and not mouse.is_button_pressed(1):
                if self.confirmaSenhaCampo.texto == self.senhaCampo.texto:
                    clicou_cadastro = False
                    sucesso, resultado = cadastro(self.loginCampo.texto, self.usernameCampo.texto, self.senhaCampo.texto)
                    if not sucesso:
                        print(resultado)
                    else:
                        self.janela.input_pygame = False
                        return estados["menu_logado"], resultado
            
            self.janela.update()

    def draw(self):
        super().draw()
        self.bg.draw()
        self.barra_superior.draw()
        self.botao_x.render()
        self.loginCampo.draw()
        self.usernameCampo.draw()
        self.confirmaSenhaCampo.draw()
        self.senhaCampo.draw()
        self.botao.render()
        #pygame.draw.rect(self.janela.get_screen(), (200,15,51),self.botao)

    def evento(self, e):
        super().evento(e)
        self.usernameCampo.evento(e)
        self.loginCampo.evento(e)
        self.senhaCampo.evento(e)
        self.confirmaSenhaCampo.evento(e)
