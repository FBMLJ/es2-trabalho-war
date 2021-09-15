from componentes.RetanguloTexto import * 
from componentes.botao import *
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.window import Window

class HudCombate:

    def __init__(self, janela:Window) -> None:
        caminho_assets = "assets/imagem/hud/"

        self.janela = janela

        self.box = GameImage(caminho_assets + "hud_combate.png")
        self.box.set_position(int(self.box.width/3.5), janela.height - self.box.height)

        self.territorio_atacante = ""
        self.territorio_defensor = ""
        self.botao_clicado = 0
        self.botao_foi_clicado = False

        self.atacante_texto = GameImage(caminho_assets + "atacante.png")
        self.atacante_texto.set_position(
                                            self.box.x + int(0.3*self.atacante_texto.width),
                                            self.box.y + int(0.3*self.atacante_texto.height)
                                        )

        self.defensor_texto = GameImage(caminho_assets + "defensor.png")
        self.defensor_texto.set_position(
                                            self.box.x + self.box.width - (self.defensor_texto.width + int(0.3*self.defensor_texto.width)),
                                            self.box.y + int(0.3*self.defensor_texto.height)
                                        )
        self.botoes = []

        botao_ok = Botao(Sprite(caminho_assets + "botao_ok.png"), Sprite(caminho_assets + "botao_ok_select.png"), 1)
        botao_ok.setposition(
                                self.atacante_texto.x + self.atacante_texto.width - botao_ok.width,
                                self.box.y + self.box.height - botao_ok.height - 5
                            )
        self.botoes.append(botao_ok)

        botao_cancela = Botao(Sprite(caminho_assets + "botao_cancela.png"), Sprite(caminho_assets + "botao_cancela_select.png"), 2)
        botao_cancela.setposition(
                                self.defensor_texto.x,
                                self.box.y + self.box.height - botao_cancela.height - 5
                            )
        self.botoes.append(botao_cancela)

        self.caixa_atacante = RetanguloTexto(self.janela, "", 0, self.atacante_texto.width, self.defensor_texto.height, 10, False)
        self.caixa_atacante.centralizado = True
        self.caixa_atacante.set_position(
                                            self.atacante_texto.x,
                                            self.atacante_texto.y + self.atacante_texto.height + int(0.3*self.caixa_atacante.height)
                                        )
        
        self.caixa_defensor = RetanguloTexto(self.janela, "", 0, self.defensor_texto.width, self.defensor_texto.height, 10, False)
        self.caixa_defensor.centralizado = True
        self.caixa_defensor.set_position(
                                            self.defensor_texto.x,
                                            self.defensor_texto.y + self.defensor_texto.height + int(0.3*self.caixa_defensor.height)
                                        )

    def update(self):
        for botao in self.botoes:
            retorno = botao.update()
            if retorno:
                self.botao_foi_clicado = True
                self.botao_clicado = botao.code

        codigo_retorno = self.botao_clicado #  0: nada foi clicado, 1: pode ocorrer combate, 2: cancela as selecoes
        self.botao_clicado = 0
        
        return codigo_retorno

    def render(self):
        self.box.draw()
        self.atacante_texto.draw()
        self.defensor_texto.draw()
        self.caixa_atacante.render()
        self.caixa_defensor.render()
        for botao in self.botoes:
            botao.render()

    def atualiza_atacante(self, atacante:str):
        self.caixa_atacante.texto = atacante
    
    def atualiza_defensor(self, defensor:str):
        self.caixa_defensor.texto = defensor