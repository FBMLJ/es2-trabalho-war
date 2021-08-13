from PPlay.window import Window
from PPlay.gameimage import GameImage
from PPlay.sprite import Sprite
from PPlay.window import Window
from componentes.icone import Icone
from componentes.botao import Botao

class hudTurno:

    def __init__(self, janela:Window):
        caminho_hud = "assets/imagem/hud/"

        self.barra = GameImage(caminho_hud+"barra_hud.png")
        self.barra.set_position(janela.width/2 - self.barra.width/2, janela.height - self.barra.height)
        offset_y = 20
        offset = 30
        dist_acc = self.barra.x + offset
        
        distribuir_normal = GameImage(caminho_hud+"botao_distribuir_block.png")
        distribuir_destacado = GameImage(caminho_hud+"botao_distribuir.png")
        self.icone_distribuir = Icone(distribuir_normal, distribuir_destacado)
        self.icone_distribuir.set_position(dist_acc, self.barra.y + offset_y )
        self.icone_distribuir.is_normal = False #  Atribuicao para mostrar no relatorio
        dist_acc += self.icone_distribuir.width + offset

        combate_normal = GameImage(caminho_hud+"botao_combate_block.png")
        combate_destacado = GameImage(caminho_hud+"botao_combate.png")
        self.icone_combate = Icone(combate_normal, combate_destacado)
        self.icone_combate.set_position(dist_acc, self.icone_distribuir.y )

        dist_acc += self.icone_combate.width + offset

        movimento_normal = GameImage(caminho_hud+"botao_movimenta_block.png")
        movimento_destacado = GameImage(caminho_hud+"botao_movimenta.png")
        self.icone_movimento = Icone(movimento_normal, movimento_destacado)
        self.icone_movimento.set_position(dist_acc, self.icone_combate.y)

        dist_acc += self.icone_movimento.width + offset

        finalizar_normal = Sprite(caminho_hud+"botao_seta.png")
        finalizar_destacado = Sprite(caminho_hud+"botao_seta.png")
        self.finalizar = Botao(finalizar_normal, finalizar_destacado, 1)
        pos_y = self.icone_movimento.y + self.icone_movimento.heigth - self.finalizar.height
        self.finalizar.setposition(dist_acc, pos_y)
    
        self.finalizar_texto = GameImage(caminho_hud+"finalizar.png")
        pos_x = self.finalizar.x + self.finalizar.width/2 - self.finalizar_texto.width/2
        self.finalizar_texto.set_position(pos_x, self.barra.y + offset_y)

        dist_acc += self.finalizar.width + offset

        pular_normal = Sprite(caminho_hud+"botao_x.png")
        pular_destacado = Sprite(caminho_hud+"botao_x.png")
        self.pular = Botao(pular_normal, pular_destacado, 2)
        self.pular.setposition(dist_acc, pos_y)

        self.pular_texto = GameImage(caminho_hud+"pular.png")
        pos_x = self.pular.x + self.pular.width/2 - self.pular_texto.width/2
        self.pular_texto.set_position(pos_x, self.barra.y + offset_y)

    def render(self):
        self.barra.draw()
        self.icone_distribuir.render()
        self.icone_combate.render()
        self.icone_movimento.render()
        self.finalizar.render()
        self.pular.render()
        self.finalizar_texto.draw()
        self.pular_texto.draw()