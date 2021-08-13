from telas.JanelaPadrao import JanelaPadrao
from PPlay.gameimage import GameImage
from PPlay.sprite import *
from componentes.botao import *
from PPlay.mouse import Mouse
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

        self.loginCampo = CampoTexto(janela,
                                     GameImage("assets/imagem/cadastro/informe_email.png"),
                                     janela.width/2 - 320, 180, 640, 60)

        self.usernameCampo = CampoTexto(janela,
                                        GameImage("assets/imagem/cadastro/informe_nome_usuario.png"),
                                        janela.width/2 - 320, 300, 640, 60)

        self.senhaCampo = CampoSenha(janela,
                                     GameImage("assets/imagem/cadastro/defina_senha.png"),
                                     janela.width/2 - 320, 420, 640, 60)

        self.confirmaSenhaCampo = CampoSenha(janela,
                                             GameImage("assets/imagem/cadastro/confirme_senha.png"),
                                             janela.width/2 - 320, 540, 640, 60)

        botao_sprite = Sprite("assets/imagem/cadastro/botao_cadastrar.png")
        botao_selecionado_sprite = Sprite("assets/imagem/cadastro/botao_cadastrar_select.png")
        self.botao = Botao(botao_sprite, botao_selecionado_sprite, estados["cadastro"])
        altura_botao = self.confirmaSenhaCampo.y + self.confirmaSenhaCampo.height + 25
        self.botao.setposition(self.janela.width/2 - self.botao.width/2, altura_botao)
        #self.botao = pygame.Rect([480,490,320,60])

        self.barra_superior = GameImage("assets/imagem/barra_superior_geral.png")

        self.titulo_janela = GameImage("assets/imagem/cadastro/letrero_cadastro.png")
        self.titulo_janela.set_position(50, self.barra_superior.height/2 - self.titulo_janela.height/2)

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
        self.titulo_janela.draw()
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
