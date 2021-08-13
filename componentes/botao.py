"""
Classe responsavel por implementar as funcionalidades de um botão da interface.
"""

from PPlay.sprite import *
from PPlay.mouse import *


class Botao:

    def __init__(self, sprite_normal: Sprite, sprite_destacado: Sprite, code: int):
        self.sprites = []
        self.sprites.append(sprite_normal)
        self.sprites.append(sprite_destacado)
        self.width = sprite_normal.width
        self.height = sprite_normal.height
        self.code = code  # atributo que guarda um codigo referente ao botao
        self.spriteAtual = 0
        self.mouse = Mouse()
        self.x = 0
        self.y = 0

    def update(self):
        if self.mouse.is_over_area(
                (self.sprites[0].x, self.sprites[0].y),
                (self.sprites[0].x + self.sprites[0].width, self.sprites[0].y + self.sprites[0].height)
        ):
            self.spriteAtual = 1
            if self.mouse.is_button_pressed(1):
                return True
        else:
            self.spriteAtual = 0

        return False

    def render(self):
        self.sprites[self.spriteAtual].draw()

    def setposition(self, x, y):
        self.sprites[0].set_position(x, y)
        self.sprites[1].set_position(x, y)
        self.x = x
        self.y = y
