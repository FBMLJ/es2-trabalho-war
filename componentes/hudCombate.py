from componentes.RetanguloTexto import * 
from componentes.botao import *
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.window import Window

class HudCombate:

    def __init__(self, janela:Window) -> None:
        self.caminho_assets = "assets/imagem/hud/"

        self.janela = janela
        self.nao_desenha = False

        self.box = GameImage(self.caminho_assets + "hud_combate.png")
        self.box.set_position(int(self.box.width/3.5), janela.height - self.box.height)

        self.etapa_combate = 0 #  variavel para indicar que componentes da hud desenhar
                               #  0: escolha de territorios atacante e defensor
                               #  1: escolha da quantidade de tropas atacantes
        self.territorio_atacante = ""
        self.territorio_defensor = ""

        self.quantidade_maxima = 0
        self.quantidade_atual = 0
        self.botao_clicado = 0
        self.botao_foi_clicado = False

        self.atacante_texto = None
        self.defensor_texto = None
        self.caixa_atacante = None
        self.caixa_defensor = None
        self.posicao_caixa_atacante = []
        self.posicao_caixa_defensor = []
        self.atacantes_texto = None
        self.caixa_quantidade_atacantes = None

        self.botoes = []

        self.inicializa_etapa_combate()


    def update(self, mouse:Mouse):

        for botao in self.botoes:
            retorno = botao.update()
            if retorno:
                self.botao_foi_clicado = True
                self.botao_clicado = botao.code
        
        codigo_retorno = 0
        if self.botao_foi_clicado and not mouse.is_button_pressed(1):
            self.botao_foi_clicado = False
            if self.etapa_combate == 0:
                codigo_retorno = self.botao_clicado #  0: nada foi clicado, 1: pode ocorrer combate, 2: cancela as selecoes
            if self.etapa_combate == 1:
                if self.botao_clicado == 4: #  Botao MAIS
                    if(self.quantidade_atual < self.quantidade_maxima):
                        self.quantidade_atual += 1
                if self.botao_clicado == 5: #  Botao MENOS
                    if(self.quantidade_atual > 0):
                        self.quantidade_atual -= 1
                self.caixa_quantidade_atacantes.texto = str(self.quantidade_atual)
            codigo_retorno = self.botao_clicado
            self.botao_clicado = 0
        
        return codigo_retorno

    def render(self):
        if self.nao_desenha:
            return
        self.box.draw()
        if(self.etapa_combate==0):
            self.atacante_texto.draw()
            self.defensor_texto.draw()
            #self.caixa_atacante.render()
            #self.caixa_defensor.render()
            self.janela.draw_text(
                self.territorio_atacante,
                self.posicao_caixa_atacante[0],
                self.posicao_caixa_atacante[1],
                bold=True
            )
            self.janela.draw_text(
                self.territorio_defensor,
                self.posicao_caixa_defensor[0],
                self.posicao_caixa_defensor[1],
                bold=True
            )
        elif(self.etapa_combate==1):
            self.atacantes_texto.draw()
            self.caixa_quantidade_atacantes.render()
        for botao in self.botoes:
            botao.render()

    def atualiza_atacante(self, atacante:str):
        self.territorio_atacante = atacante
        self.caixa_atacante.texto = atacante
    
    def atualiza_defensor(self, defensor:str):
        self.territorio_defensor = defensor
        self.caixa_defensor.texto = defensor
    
    def set_etapa_combate(self, etapa:int):
        if self.etapa_combate != etapa:
            self.etapa_combate = etapa
        self.inicializa_etapa_combate()

    def inicializa_etapa_combate(self):
        self.nao_desenha = False
        if self.etapa_combate == 0:
            self.inicializa_etapa_combate_0()
        if self.etapa_combate == 1:
            self.inicializa_etapa_combate_1()

    def inicializa_etapa_combate_0(self):

        self.atacantes_texto = None
        self.caixa_quantidade_atacantes = None

        self.botoes.clear()

        self.atacante_texto = GameImage(self.caminho_assets + "atacante.png")
        self.atacante_texto.set_position(
                                            self.box.x + int(0.25*self.box.width) - int(self.atacante_texto.width/2),
                                            self.box.y + int(0.1*self.box.height)
                                        )

        self.defensor_texto = GameImage(self.caminho_assets + "defensor.png")
        self.defensor_texto.set_position(
                                            self.box.x + int(0.75*self.box.width) - int(self.defensor_texto.width/2),
                                            self.box.y + int(0.1*self.box.height)
                                        )

        botao_ok = Botao(Sprite(self.caminho_assets + "botao_ok.png"), Sprite(self.caminho_assets + "botao_ok_select.png"), 1)
        botao_ok.setposition(
                                self.atacante_texto.x,
                                self.box.y + self.box.height - botao_ok.height - 5
                            )
        self.botoes.append(botao_ok)

        botao_cancela = Botao(Sprite(self.caminho_assets + "botao_cancela.png"), Sprite(self.caminho_assets + "botao_cancela_select.png"), 2)
        botao_cancela.setposition(
                                self.defensor_texto.x + self.defensor_texto.width - botao_cancela.width,
                                self.box.y + self.box.height - botao_cancela.height - 5
                            )

        self.botoes.append(botao_cancela)

        self.caixa_atacante = RetanguloTexto(self.janela, "", 1, self.atacante_texto.width, self.defensor_texto.height, 10, False)
        self.caixa_atacante.centralizado = True
        self.caixa_atacante.set_position(
                                            self.atacante_texto.x + int(self.atacante_texto.width/2) - int(self.caixa_atacante.width/2),
                                            self.atacante_texto.y + self.atacante_texto.height + int(0.3*self.caixa_atacante.height)
                                        )
        self.posicao_caixa_atacante = [self.caixa_atacante.x, self.caixa_atacante.y]

        self.caixa_defensor = RetanguloTexto(self.janela, "", 2, self.defensor_texto.width, self.defensor_texto.height, 10, False)
        self.caixa_defensor.centralizado = True
        self.caixa_defensor.set_position(
                                            self.defensor_texto.x + int(self.defensor_texto.width/2) - int(self.caixa_defensor.width/2),
                                            self.defensor_texto.y + self.defensor_texto.height + int(0.3*self.caixa_defensor.height)
                                        )
        self.posicao_caixa_defensor = [self.caixa_defensor.x, self.caixa_defensor.y]
    
    def inicializa_etapa_combate_1(self):

        self.atacante_texto = None
        self.defensor_texto = None
        self.caixa_atacante = None
        self.caixa_defensor = None

        self.botoes.clear()

        self.atacantes_texto = GameImage(self.caminho_assets + "atacantes.png")
        self.atacantes_texto.set_position(
                                            self.box.x + int(self.box.width/2) - int(self.atacantes_texto.width/2),
                                            self.box.y + int(0.4*self.atacantes_texto.height)
                                        )

        self.caixa_quantidade_atacantes = RetanguloTexto(self.janela, "", 3, self.atacantes_texto.width, self.atacantes_texto.height, 10, False)
        self.caixa_quantidade_atacantes.centralizado = True
        self.caixa_quantidade_atacantes.set_position(
                                                        self.atacantes_texto.x,
                                                        self.atacantes_texto.y + int(1.4*self.atacantes_texto.height)
                                                    )

        botao_ok_2 = Botao(Sprite(self.caminho_assets + "botao_ok.png"), Sprite(self.caminho_assets + "botao_ok_select.png"), 3)
        botao_ok_2.setposition(
                                self.box.x + int(self.box.width/2) - int(botao_ok_2.width/2),
                                self.box.y + self.box.height - int(1.2*botao_ok_2.height)
                              )
        self.botoes.append(botao_ok_2)

        botao_mais = Botao(Sprite(self.caminho_assets + "botao_mais_combate.png"), Sprite(self.caminho_assets + "botao_mais_combate_select.png"), 4)
        botao_mais.setposition(
                                self.caixa_quantidade_atacantes.x + self.caixa_quantidade_atacantes. width + int(0.2*botao_mais.width),
                                self.caixa_quantidade_atacantes.y
                              )
        self.botoes.append(botao_mais)

        botao_menos = Botao(Sprite(self.caminho_assets + "botao_menos_combate.png"), Sprite(self.caminho_assets + "botao_menos_combate_select.png"), 5)
        botao_menos.setposition(
                                self.caixa_quantidade_atacantes.x -( botao_menos.width + int(0.2*botao_menos.width) ),
                                self.caixa_quantidade_atacantes.y
                                )
        self.botoes.append(botao_menos)

    def limpa_hud(self):
        self.botoes.clear()

        self.atacante_texto = None
        self.defensor_texto = None
        self.caixa_atacante = None
        self.caixa_defensor = None

        self.atacantes_texto = None
        self.caixa_quantidade_atacantes = None

        self.nao_desenha = True