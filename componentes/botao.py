from PPlay.sprite import *
from PPlay.mouse import *
"""
Classe responsavel por implementar as funcionalidades de um botão da interface.
"""

class Button:

    def __init__(self, caminhos, code):
        self.sprites = []
        self.sprites.append(Sprite(caminhos[0]))
        self.sprites.append(Sprite(caminhos[1]))
        self.width = self.sprites[0].width
        self.height = self.sprites[0].height
        self.code = code
        self.spriteAtual = 0
        self.mouse = Mouse()

    def update(self):
        if self.mouse.is_over_area((self.sprites[0].x, self.sprites[0].y), (self.sprites[0].x + self.sprites[0].width,
                                                                            self.sprites[0].y + self.sprites[
                                                                                0].height)):
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
