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
        self.barra_superior.set_position(self.fundo.x + 12, self.fundo.y + 10)

        sprite_x = Sprite("assets/imagem/saguao/x_saguao.png")
        botao_x = Botao(sprite_x, sprite_x, self.codigo_botoes["sair"])
        botao_x.setposition(self.fundo.x + self.fundo.width - botao_x.width - 16, self.fundo.y + 15)
        self.botoes.append(botao_x)

        sprite_enviar_normal = Sprite("assets/imagem/saguao/botao_enviar.png")
        sprite_enviar_destacado = Sprite("assets/imagem/saguao/botao_enviar_select.png")
        botao_enviar = Botao(sprite_enviar_normal, sprite_enviar_destacado, self.codigo_botoes["enviar"])
        botao_enviar.setposition(
            self.fundo.x + self.fundo.width - botao_enviar.width - 40,
            self.fundo.y + self.fundo.height - botao_enviar.height - 40
        )
        self.botoes.append(botao_enviar)

        sprite_pronto_normal = Sprite("assets/imagem/saguao/botao_pronto.png")
        sprite_pronto_destacado = Sprite("assets/imagem/saguao/botao_pronto_select.png")
        botao_pronto = Botao(sprite_pronto_normal, sprite_pronto_destacado, self.codigo_botoes["pronto"])
        botao_pronto.setposition(
            self.fundo.x + 80,
            self.fundo.y + self.fundo.height - botao_pronto.height - 40
        )
        self.botoes.append(botao_pronto)

        self.campo_chat = CampoTexto(
            janela,
            GameImage("assets/imagem/saguao/digite_mensagem.png"),
            self.fundo.x + self.fundo.width - 640,
            self.fundo.y + self.fundo.height - botao_pronto.height - 36,
            450,
            50,
            25
        )

        self.legenda_participantes = GameImage("assets/imagem/saguao/participantes.png")
        self.legenda_participantes.set_position(
            self.fundo.x + 50,
            self.barra_superior.y + self.barra_superior.height + 10
        )

        self.legenda_chat = GameImage("assets/imagem/saguao/chat.png")
        self.legenda_chat.set_position(
            self.fundo.x + self.fundo.width - self.legenda_chat.width - 300,
            self.barra_superior.y + self.barra_superior.height + 10
        )

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
            self.campo_chat.evento(evento)
            if evento.type == pygame.QUIT:
                exit()

    def render(self):

        self.fundo.draw()
        self.barra_superior.draw()
        self.campo_chat.draw()
        self.legenda_participantes.draw()
        self.legenda_chat.draw()
        for botao in self.botoes:
            botao.render()
