from componentes.campoTexto import *
from componentes.botao import *
from PPlay.gameimage import *
from PPlay.sprite import *


class Saguao:

    def __init__(self, janela):

        self.janela = janela
        self.fundo = GameImage("assets/imagem/saguao/saguao.png")
        self.fundo.set_position(janela.width/2 - self.fundo.width/2, self.janela.height/2 - self.fundo.height/2)

        self.codigo_botoes = {
            "sair": 1,
            "pronto": 2,
            "enviar": 3
        }

        self.botoes = []

        self.barra_superior = GameImage("assets/imagem/saguao/barra_saguao.png")
        self.barra_superior.set_position(self.fundo.x + 16, self.fundo.y + 10)

        sprite_x = Sprite("assets/imagem/busca_saguao/x_saguao.png")
        botao_x = Botao(sprite_x, sprite_x, self.codigo_botoes["sair"])
        botao_x.setposition(self.fundo.x + self.fundo.width - botao_x.width - 20, self.fundo.y + 15)
        self.botoes.append(botao_x)

    def loop(self):

        self.janela.clear()
        self.janela.set_background_color([0, 0, 0])
        self.janela.input_pygame = True

        botao_clicado = -1
        clicou = False
        mouse = Mouse()

        while True:

            for botao in self.botoes:
                clicou = botao.update()
                if clicou:
                    botao_clicado = botao.code

            if clicou and mouse.is_button_pressed(1):
                if botao_clicado == self.codigo_botoes["sair"]:
                    self.janela.input_pygame = False
                    return

            self.trataEvento()
            self.render()
            self.janela.update()

    def trataEvento(self):

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                exit()

    def render(self):

        self.fundo.draw()
        self.barra_superior.draw()
        for botao in self.botoes:
            botao.render()
