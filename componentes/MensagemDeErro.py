from PPlay.gameimage import *
from PPlay.window import *
from componentes.botao import *

'''
Classe para definir o componente que envia uma mensagem de erro e espera uma confirmação
'''


class MensagemDeErro:
    # Inicia o objeto com seus respectivos sprites, fundo e inputs nas posicoes corretas
    def __init__(self, janela: Window, mensagem: str):

        self.janela = janela

        self.fundo = GameImage("assets/imagem/busca_saguao/sombra.png")

        self.popup_box = GameImage("assets/imagem/busca_saguao/popup.png")
        self.popup_box.set_position(
            janela.width / 2 - self.popup_box.width / 2,
            self.janela.height / 2 - self.popup_box.height / 2
        )

        self.mensagem = mensagem

        self.ok_botao = Botao(
            Sprite("assets/imagem/busca_saguao/botao_ok.png"),
            Sprite("assets/imagem/busca_saguao/botao_ok_select.png"),
            1
        )
        self.ok_botao.setposition(
            self.popup_box.x + self.popup_box.width / 2 - self.ok_botao.width / 2,
            self.popup_box.y + self.popup_box.height - 45
        )

    # Atualiza os componentes do popup a cada frame
    def update(self):

        codigo_retorno = self.ok_botao.update()
        if codigo_retorno:
            return self.ok_botao.code

        return 0

    # Renderiza os objetos do popup
    def render(self):

        self.fundo.draw()
        self.popup_box.draw()
        self.ok_botao.render()
        self.janela.draw_text(self.mensagem,
                              self.popup_box.x + self.popup_box.width/2 - len(self.mensagem)*4.3,
                              self.popup_box.y + self.popup_box.height/2 - 25, size=18, color=[255, 255, 255])
