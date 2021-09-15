from componentes.RetanguloTexto import * 
from componentes.botao import *
from PPlay.gameimage import *
from PPlay.sprite import *
from PPlay.window import Window

class HudSelecionaTropas:

    def __init__(self, janela:Window):
        caminho_assets = "assets/imagem/hud/"

        self.janela = janela

        self.box = GameImage(caminho_assets + "hud_seleciona_tropas.png")
        self.box.set_position(int(self.box.width/3.5), janela.height - self.box.height)

        self.quantidade = 0 #  Quantidade de tropas a colocar num territorio selecionado
        self.maximo = 0 #  Quantidade maxima de tropas que o jogador pode colocar neste turno
        self.botao_clicado = 0
        self.botao_foi_clicado = False
        self.mouse = Mouse()

        self.botoes = []

        botao_ok = Botao(Sprite(caminho_assets + "botao_ok.png"), Sprite(caminho_assets + "botao_ok_select.png"), 3)
        botao_ok.setposition(
                                self.box.x + self.box.width/2 - botao_ok.width/2,
                                self.box.y + self.box.height - botao_ok.height - 5
                            )
        self.botoes.append(botao_ok)
        
        distancia = (botao_ok.x - self.box.x)/2

        botao_mais = Botao(Sprite(caminho_assets + "botao_mais.png"), Sprite(caminho_assets + "botao_mais_select.png"), 1)
        botao_mais.setposition(
                                botao_ok.x + botao_ok.width + distancia - botao_mais.width/2, 
                                self.box.y + self.box.height/2 - botao_mais.height/2  
                              )
        self.botoes.append(botao_mais)

        botao_menos = Botao(Sprite(caminho_assets + "botao_menos.png"), Sprite(caminho_assets + "botao_menos_select.png"), 2)
        botao_menos.setposition(
                                self.box.x + distancia - botao_menos.width/2,              
                                self.box.y + self.box.height/2 - botao_menos.height/2
                                )
        self.botoes.append(botao_menos)
        

        self.caixa_quantidade = RetanguloTexto(self.janela,str(self.quantidade),0,botao_ok.width,30,25,False)
        self.caixa_quantidade.centralizado = True
        self.caixa_quantidade.set_position(self.box.x + self.box.width/2 - self.caixa_quantidade.width/2, self.box.y + 20)

    
    def update(self, mouse:Mouse):

        for botao in self.botoes:
            retorno = botao.update()
            if retorno:
                self.botao_foi_clicado = True
                self.botao_clicado = botao.code
        
        if self.botao_foi_clicado and not mouse.is_button_pressed(1):
            self.botao_foi_clicado = False
            if self.botao_clicado == 1: #  Botao mais
                if self.quantidade < self.maximo:
                    self.quantidade += 1
            elif self.botao_clicado == 2: #  Botao menos
                if self.quantidade > 0:
                    self.quantidade -= 1
            elif self.botao_clicado == 3: #  Botao ok
                self.botao_clicado = 0
                return True #  Somente retorna TRUE quando o ok for clicado
            
            #print("quantidade: {}".format(self.quantidade))

            self.caixa_quantidade.texto = str(self.quantidade)
            self.botao_clicado = 0
        
        return False


    def render(self):
        self.box.draw()
        self.caixa_quantidade.render()
        for botao in self.botoes:
            botao.render()