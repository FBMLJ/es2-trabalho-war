from componentes.hudCartas import HudCartas
from jogo.Player import Player
from jogo.CardManager import CardManager
from PPlay.mouse import Mouse
from PPlay.gameimage import GameImage
from PPlay.window import Window

class ControladorCartas:
    
    def __init__(self):
        caminho_hud = "assets/imagem/hud/"
        caminho_cartas = "assets/imagem/cartas/"
        self.hud_cartas = HudCartas()
        self.cartas_selecionadas = []
        self.colisao_mouse = GameImage(caminho_hud+"mouse_colisao.jpg")
        self.carta_selecionada = GameImage(caminho_cartas+"card_select.png")
    
    def selecionar_cartas(self, mouse:Mouse, jogador:Player):
        x,y = mouse.get_position()
        self.colisao_mouse.set_position(x,y)
        if mouse.is_button_pressed(1) and self.hud_cartas.mostrar_cartas:
            self.colisao_mouse.draw()
            for carta in jogador.cartas:
                if(
                    self.colisao_mouse.collided_perfect(carta.img) and
                    len(self.cartas_selecionadas) < 3 and
                    carta not in self.cartas_selecionadas
                ):
                    self.cartas_selecionadas.append(carta)
    

    def update(self, mouse:Mouse):
        retorno = self.hud_cartas.update(mouse)
        if retorno == 1:
            self.hud_cartas.cria() #  Abrir o menu de cartas
        if retorno == 2:
            return 1 #  Somente retorna TRUE quando o jogador tenta trocar as cartas
        if retorno == 3:
            self.cartas_selecionadas = [] #  Cancelar a selecao feita
        if retorno == 4:
            self.cartas_selecionadas = []
            self.hud_cartas.limpa() #  Fechar o menur de cartas
            return 2 
        return 0

    def render(self, jogador:Player):
        
        self.hud_cartas.render(jogador)
        for carta in self.cartas_selecionadas:
            carta.img_select.set_position(carta.img.x, carta.img.y)
            carta.img_select.draw()

    def jogador_deve_trocar(self, jogador:Player):
        if len(jogador.cartas) >= 5:
            return True
        return False

    def forca_troca(self, jogador:Player):
        self.hud_cartas.cria()
        self.hud_cartas.deve_trocar = True 