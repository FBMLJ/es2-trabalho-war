from componentes.botao import Botao
from PPlay.gameimage import GameImage
from PPlay.sprite import Sprite
from PPlay.mouse import Mouse
from jogo.Player import Player

class hudTroca:
    def __init__(self):
        caminho_hud = "assets/imagem/hud/"
        #179 x 279
        self.mostrar_cartas = False
        self.cartas_selecionados = []

        self.hud_trocas = GameImage("") # Fundo para a exibicao das cartas

        self.botao_mostrar_menu = Botao(
            Sprite(caminho_hud + "botao_deck.png"), 
            Sprite(caminho_hud + "botao_deck_select"), 
            1
        )

        self.botoes = []

        botao_realizar_troca = Botao(Sprite(""), Sprite(""), 2)
        self.botoes.append(botao_realizar_troca)

        botao_cancelar_troca = Botao(Sprite(""), Sprite(""), 3)
        self.botoes.append(botao_cancelar_troca)
        
        botao_voltar_menu = Botao(Sprite(""), Sprite(""), 4)
        self.botoes.append(botao_voltar_menu)

    def update(self, mouse:Mouse):
        for botao in self.botoes:
            retorno = botao.update()
            if retorno:
                self.botao_foi_clicado = True
                self.botao_clicado = botao.code
        
        if self.botao_foi_clicado and not mouse.is_button_pressed(1):
            self.botao_foi_clicado = False
            if self.botao_clicado == 2: #  Somente retorna TRUE quando
                self.botao_clicado = 0
                return True
            if self.botao_clicado == 4:
                self.mostrar_cartas = False
            self.botao_clicado = 0
        
        return False

    def render(self):
        self.botao_mostrar_menu.render()
        if self.mostrar_cartas:
            self.hud_trocas.draw()
            for botao in self.botoes:
                botao.render()
        return

    def desenha_cartas(self, jogador:Player):
        for carta in jogador.cartas:
            carta.img.draw()