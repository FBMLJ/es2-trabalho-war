from componentes.RetanguloTexto import * 
from componentes.botao import *
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.window import Window

class HudMovimenta:

    def __init__(self, janela:Window) -> None:
        self.caminho_assets = "assets/imagem/hud/"

        self.janela = janela
        self.nao_desenha = False

        self.box = GameImage(self.caminho_assets + "hud_combate.png")
        self.box.set_position(int(self.box.width/3.5), janela.height - self.box.height)

        self.etapa_movimenta = 0 #  variavel para indicar que componentes da hud desenhar
                               #  0: escolha de territorios de retirada e recepcao
                               #  1: escolha da quantidade de tropas movidas
        self.territorio_atacante = ""
        self.territorio_defensor = ""

        self.quantidade_maxima = 0
        self.quantidade_atual = 0
        self.botao_clicado = 0
        self.botao_foi_clicado = False

        self.terr_inicial_texto = None
        self.terr_destino_texto = None
        self.caixa_terr_inicial = None
        self.caixa_terr_destino = None
        self.pos_inicial = []
        self.pos_destino = []
        self.quantidade_texto = None
        self.caixa_quantidade = None

        self.botoes = []

        self.inicializa_etapa_movimenta()


    def update(self, mouse:Mouse):

        for botao in self.botoes:
            retorno = botao.update()
            if retorno:
                self.botao_foi_clicado = True
                self.botao_clicado = botao.code
        
        codigo_retorno = 0
        if self.botao_foi_clicado and not mouse.is_button_pressed(1):
            self.botao_foi_clicado = False
            if self.etapa_movimenta == 0:
                codigo_retorno = self.botao_clicado #  0: nada foi clicado, 1: pode ocorrer combate, 2: cancela as selecoes
            if self.etapa_movimenta == 1:
                if self.botao_clicado == 4: #  Botao MAIS
                    if(self.quantidade_atual < self.quantidade_maxima):
                        self.quantidade_atual += 1
                if self.botao_clicado == 5: #  Botao MENOS
                    if(self.quantidade_atual > 0):
                        self.quantidade_atual -= 1
                self.caixa_quantidade.texto = str(self.quantidade_atual)
            codigo_retorno = self.botao_clicado
            self.botao_clicado = 0
        
        return codigo_retorno

    def render(self):
        if self.nao_desenha:
            return
        self.box.draw()
        if(self.etapa_movimenta==0):
            self.terr_inicial_texto.draw()
            self.terr_destino_texto.draw()
            #self.caixa_terr_inicial.render()
            #self.caixa_terr_destino.render()
            self.janela.draw_text(
                self.caixa_terr_inicial.texto,
                self.pos_inicial[0],
                self.pos_inicial[1],
                bold=True
            )
            self.janela.draw_text(
                self.caixa_terr_destino.texto,
                self.pos_destino[0],
                self.pos_destino[1],
                bold=True
            )
        elif(self.etapa_movimenta==1):
            self.quantidade_texto.draw()
            self.caixa_quantidade.render()
        for botao in self.botoes:
            botao.render()

    def atualiza_inicial(self, terr_inicial:str):
        self.caixa_terr_inicial.texto = terr_inicial
    def atualiza_destino(self, terr_destino:str):
        self.caixa_terr_destino.texto = terr_destino
    
    def set_etapa_movimenta(self, etapa:int):
        if self.etapa_movimenta != etapa:
            self.etapa_movimenta = etapa
        self.inicializa_etapa_movimenta()

    def inicializa_etapa_movimenta(self):
        self.nao_desenha = False
        if self.etapa_movimenta == 0:
            self.inicializa_etapa_movimenta_0()
        if self.etapa_movimenta == 1:
            self.inicializa_etapa_movimenta_1()

    def inicializa_etapa_movimenta_0(self):

        self.quantidade_texto = None
        self.caixa_quantidade = None

        self.botoes.clear()

        self.terr_inicial_texto = GameImage(self.caminho_assets + "inicial.png")
        self.terr_inicial_texto.set_position(
                                            self.box.x + int(0.25*self.box.width) - int(self.terr_inicial_texto.width/2),
                                            self.box.y + int(0.1*self.box.height)
                                        )

        self.terr_destino_texto = GameImage(self.caminho_assets + "destino.png")
        self.terr_destino_texto.set_position(
                                            self.box.x + int(0.75*self.box.width) - int(self.terr_destino_texto.width/2),
                                            self.box.y + int(0.1*self.box.height)
                                        )

        botao_ok = Botao(Sprite(self.caminho_assets + "botao_ok.png"), Sprite(self.caminho_assets + "botao_ok_select.png"), 1)
        botao_ok.setposition(
                                self.terr_inicial_texto.x,
                                self.box.y + self.box.height - botao_ok.height - 5
                            )
        self.botoes.append(botao_ok)

        botao_cancela = Botao(Sprite(self.caminho_assets + "botao_cancela.png"), Sprite(self.caminho_assets + "botao_cancela_select.png"), 2)
        botao_cancela.setposition(
                                self.terr_destino_texto.x + self.terr_destino_texto.width - botao_cancela.width,
                                self.box.y + self.box.height - botao_cancela.height - 5
                            )

        self.botoes.append(botao_cancela)

        self.caixa_terr_inicial = RetanguloTexto(self.janela, "", 1, self.terr_inicial_texto.width, self.terr_destino_texto.height, 10, False)
        self.caixa_terr_inicial.centralizado = True
        self.caixa_terr_inicial.set_position(
                                            self.terr_inicial_texto.x + int(self.terr_inicial_texto.width/2) - int(self.caixa_terr_inicial.width/2),
                                            self.terr_inicial_texto.y + self.terr_inicial_texto.height + int(0.3*self.caixa_terr_inicial.height)
                                        )
        self.pos_inicial = [self.caixa_terr_inicial.x, self.caixa_terr_inicial.y]

        self.caixa_terr_destino = RetanguloTexto(self.janela, "", 2, self.terr_destino_texto.width, self.terr_destino_texto.height, 10, False)
        self.caixa_terr_destino.centralizado = True
        self.caixa_terr_destino.set_position(
                                            self.terr_destino_texto.x + int(self.terr_destino_texto.width/2) - int(self.caixa_terr_destino.width/2),
                                            self.terr_destino_texto.y + self.terr_destino_texto.height + int(0.3*self.caixa_terr_destino.height)
                                        )
        self.pos_destino = [self.caixa_terr_destino.x, self.caixa_terr_destino.y]

    def inicializa_etapa_movimenta_1(self):

        self.terr_inicial_texto = None
        self.terr_destino_texto = None
        self.caixa_terr_inicial = None
        self.caixa_terr_destino = None

        self.botoes.clear()

        self.quantidade_texto = GameImage(self.caminho_assets + "Quantidade.png")
        self.quantidade_texto.set_position(
                                            self.box.x + int(self.box.width/2) - int(self.quantidade_texto.width/2),
                                            self.box.y + int(0.4*self.quantidade_texto.height)
                                        )

        self.caixa_quantidade = RetanguloTexto(self.janela, "", 3, self.quantidade_texto.width, self.quantidade_texto.height, 10, False)
        self.caixa_quantidade.centralizado = True
        self.caixa_quantidade.set_position(
                                                        self.quantidade_texto.x,
                                                        self.quantidade_texto.y + int(1.4*self.quantidade_texto.height)
                                                    )

        botao_ok_2 = Botao(Sprite(self.caminho_assets + "botao_ok.png"), Sprite(self.caminho_assets + "botao_ok_select.png"), 3)
        botao_ok_2.setposition(
                                self.box.x + int(self.box.width/2) - int(botao_ok_2.width/2),
                                self.box.y + self.box.height - int(1.2*botao_ok_2.height)
                              )
        self.botoes.append(botao_ok_2)

        botao_mais = Botao(Sprite(self.caminho_assets + "botao_mais_combate.png"), Sprite(self.caminho_assets + "botao_mais_combate_select.png"), 4)
        botao_mais.setposition(
                                self.caixa_quantidade.x + self.caixa_quantidade. width + int(0.2*botao_mais.width),
                                self.caixa_quantidade.y
                              )
        self.botoes.append(botao_mais)

        botao_menos = Botao(Sprite(self.caminho_assets + "botao_menos_combate.png"), Sprite(self.caminho_assets + "botao_menos_combate_select.png"), 5)
        botao_menos.setposition(
                                self.caixa_quantidade.x -( botao_menos.width + int(0.2*botao_menos.width) ),
                                self.caixa_quantidade.y
                                )
        self.botoes.append(botao_menos)

    def limpa_hud(self):

        self.terr_inicial_texto = None
        self.terr_destino_texto = None
        self.caixa_terr_inicial = None
        self.caixa_terr_destino = None

        self.quantidade_texto = None
        self.caixa_quantidade = None

        self.botoes.clear()

        self.nao_desenha = True