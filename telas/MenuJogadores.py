from componentes.RetanguloTexto import * 
from componentes.botao import *
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.window import Window

class MenuJogadores:

    def __init__(self, janela:Window) -> None:
        caminho_assets = "assets/imagem/hud/"

        self.janela = janela
        self.nao_desenha = False

        self.fundo = GameImage("assets/imagem/tela_inicial/fundo.png")
        self.logo = GameImage("assets/imagem/tela_inicial/war.png")
        self.logo.set_position(
            self.janela.width/2-self.logo.width/2,
            self.janela.height/4-self.logo.height/2
        )

        self.box = GameImage(caminho_assets + "barra_hud_jogadores.png")
        self.box.set_position(
            self.logo.x + int(self.logo.width/2) - int(self.box.width/2),
            self.logo.y + int(1.1*self.logo.height)
        )

        self.quantidade_maxima = 6
        self.qnt_jogadores = 1
        self.qnt_bots = 0
        self.botao_clicado = 0
        self.botao_foi_clicado = False

        self.jogadores_texto = GameImage(caminho_assets + "jogadores.png")
        self.jogadores_texto.set_position(
            self.box.x + int(self.box.width/2) - int(self.jogadores_texto.width/2),
            self.box.y + int(0.1*self.box.height)
        )
        
        self.caixa_jogadores = RetanguloTexto(self.janela, str(self.qnt_jogadores), 1, int(self.jogadores_texto.width/2), self.jogadores_texto.height, moldura=True)
        self.caixa_jogadores.centralizado = True
        self.caixa_jogadores.set_position(
            self.jogadores_texto.x + int(self.jogadores_texto.width/2) - int(self.caixa_jogadores.width/2),
            self.jogadores_texto.y + int(1.1*self.jogadores_texto.height)
        )

        self.bots_texto = GameImage(caminho_assets + "bots.png")
        self.bots_texto.set_position(
            self.box.x + int(self.box.width/2) - int(self.bots_texto.width/2),
            self.box.y + int(self.box.height/2) - int(self.bots_texto.height/2)
        )

        self.caixa_bots = RetanguloTexto(self.janela, str(self.qnt_bots), 1, self.caixa_jogadores.width, self.caixa_jogadores.height, moldura=True)
        self.caixa_bots.centralizado = True
        self.caixa_bots.set_position(
            self.bots_texto.x + int(self.bots_texto.width/2) - int(self.caixa_bots.width/2),
            self.bots_texto.y + int(1.1*self.bots_texto.height)
        )
        

        self.botoes = []

        botao_mais_jogador = Botao(Sprite(caminho_assets + "botao_mais.png"), Sprite(caminho_assets + "botao_mais_select.png"), 1)
        botao_mais_jogador.setposition(
            self.box.x + int(0.75*self.box.width) - int(botao_mais_jogador.width/2),
            self.caixa_jogadores.y
        )
        self.botoes.append(botao_mais_jogador)

        botao_menos_jogador = Botao(Sprite(caminho_assets + "botao_menos.png"), Sprite(caminho_assets + "botao_menos_select.png"), 2)
        botao_menos_jogador.setposition(
            self.box.x + int(0.25*self.box.width) - int(botao_menos_jogador.width/2),
            self.caixa_jogadores.y
        )
        self.botoes.append(botao_menos_jogador)

        botao_mais_bots = Botao(Sprite(caminho_assets + "botao_mais.png"), Sprite(caminho_assets + "botao_mais_select.png"), 3)
        botao_mais_bots.setposition(
            self.box.x + int(0.75*self.box.width) - int(botao_mais_bots.width/2),
            self.caixa_bots.y
        )
        self.botoes.append(botao_mais_bots)

        botao_menos_bots = Botao(Sprite(caminho_assets + "botao_menos.png"), Sprite(caminho_assets + "botao_menos_select.png"), 4)
        botao_menos_bots.setposition(
            self.box.x + int(0.25*self.box.width) - int(botao_menos_bots.width/2),
            self.caixa_bots.y
        )
        self.botoes.append(botao_menos_bots)

        botao_ok = Botao(Sprite(caminho_assets + "botao_ok.png"), Sprite(caminho_assets + "botao_ok_select.png"), 5)
        botao_ok.setposition(
            self.box.x + int(0.75*self.box.width) - int(botao_ok.width/2),
            self.box.y + self.box.height - int(0.1*self.box.height) - botao_ok.height
        )
        self.botoes.append(botao_ok)

        botao_cancela = Botao(Sprite(caminho_assets + "botao_cancela.png"), Sprite(caminho_assets + "botao_cancela_select.png"), 6)
        botao_cancela.setposition(
            self.box.x + int(0.25*self.box.width) - int(botao_cancela.width/2),
            self.box.y + self.box.height - int(0.1*self.box.height) - botao_cancela.height
        )
        self.botoes.append(botao_cancela)

    def loop(self):
        self.janela.clear()
        mouse = Mouse()


        while True:

            for botao in self.botoes:
                retorno = botao.update()
                if retorno:
                    self.botao_foi_clicado = True
                    self.botao_clicado = botao.code
            
            if self.botao_foi_clicado and not mouse.is_button_pressed(1):
                self.botao_foi_clicado = False

                if self.botao_clicado == 1: #  Botao MAIS jogador
                    if self.qnt_jogadores < self.quantidade_maxima:
                        self.qnt_jogadores += 1
                        if self.qnt_jogadores + self.qnt_bots > self.quantidade_maxima:
                            self.qnt_bots -= 1

                elif self.botao_clicado == 2: #  Botao MENOS jogador
                    if self.qnt_jogadores > 1:
                        self.qnt_jogadores -= 1
                        
                elif self.botao_clicado == 3: #  Botao MAIS bot
                    if self.qnt_bots < self.quantidade_maxima:
                        self.qnt_bots += 1
                        if self.qnt_bots + self.qnt_jogadores > self.quantidade_maxima:
                            self.qnt_jogadores -= 1

                elif self.botao_clicado == 4: #  Botao MENOS bot
                    if self.qnt_bots > 0:
                        self.qnt_bots -= 1

                elif self.botao_clicado == 5: #  Botao OK
                    #  O jogo so pode comecar com pelo menos quatro jogadores e um jogador real
                    if (self.qnt_jogadores + self.qnt_bots >= 4) and self.qnt_jogadores >= 1:
                        self.botao_clicado = 0
                        return 0 #  Somente retorna 1 quando o OK for clicado
                        
                elif self.botao_clicado == 6: #  Botao CANCELA
                    self.botao_clicado = 0
                    return 1 #  Retorna 1 para voltar ao menur inicial

                self.atualiza_caixas()
                self.botao_clicado = 0
            
            self.render()
            self.janela.update()
    
    def atualiza_caixas(self):
        self.caixa_jogadores.texto = str(self.qnt_jogadores)
        self.caixa_bots.texto = str(self.qnt_bots)

    def render(self):
        self.fundo.draw()
        self.logo.draw()
        self.box.draw()
        self.jogadores_texto.draw()
        self.bots_texto.draw()
        self.caixa_jogadores.render()
        self.caixa_bots.render()
        for botao in self.botoes:
            botao.render()

    def limpa_hud(self):

        self.box = None
        self.quantidade_maxima = 6
        self.qnt_jogadores = 0
        self.qnt_bots = 0
        self.botao_clicado = 0
        self.botao_foi_clicado = False

        self.jogadores_texto = None
        
        self.caixa_jogadores = None

        self.bots_texto = None

        self.caixa_bots = None

        self.botoes.clear()