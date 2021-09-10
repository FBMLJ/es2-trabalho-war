"""
Classe responsavel por mostrar exibir e gerenciar o LogIn do jogo.
"""
from telas.JanelaPadrao import JanelaPadrao
from PPlay.gameimage import GameImage
from componentes.botao import *
from constant import estados
from componentes.campoTexto import CampoTexto
from componentes.campoSenha import CampoSenha
from servico.Login import sign_in


class Login(JanelaPadrao):

    def __init__(self, janela):

        # instancia os componentes da interface
        super().__init__(janela)
        self.bg = GameImage(image_file="./assets/imagem/tela_inicial/fundo.png")
        self.bg.set_scale(self.janela.width, self.janela.height)

        titulo = GameImage("assets/imagem/Login/email.png")
        self.loginCampo = CampoTexto(janela, titulo, janela.width/2 - 320, 240, 640, 60, 35)

        titulo = GameImage("assets/imagem/Login/senha.png")
        self.senhaCampo = CampoSenha(janela, titulo, janela.width/2 - 320, 380, 640, 60, 35)

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

        # indica que a classe irá tratar os inputs do pygame
        # necessário para interfaces com campos de input
        self.janela.input_pygame = True

        clicou_login = False
        mouse = Mouse()

        while True:
            self.draw()

            # verifica se o usuário clicou no botão de sair
            saiu = self.botao_x.update()
            if saiu:
                # se o usuário clicou no botão de sair, retorna ao menu inicial
                self.janela.input_pygame = False
                return estados["menu_inicial"], None

            # lógica que impede que o botão de login seja clicado várias vezes
            logar = self.botao_login.update()
            if logar:
                clicou_login = True

            # se clicou no login e soltou o botão do mouse, tenta fazer o login no sistema.
            if clicou_login and not mouse.is_button_pressed(1):
                sucesso, resultado = sign_in(self.loginCampo.texto, self.senhaCampo.texto)
                clicou_login = False
                # se o login falhou, printa o erro
                if not sucesso:
                    print(resultado)
                else:
                    # se o login foi bem sucedido, envia para o menu logado
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
        self.senhaCampo.draw()
        self.botao_login.render()

    # funcao que trata os eventos do pygame
    # necessario para formulario
    def evento(self, e):
        super().evento(e)
        self.loginCampo.evento(e)
        self.senhaCampo.evento(e)
