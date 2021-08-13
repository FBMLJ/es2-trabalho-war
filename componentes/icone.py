from PPlay.gameimage import GameImage

class Icone:
    
    def __init__(self, img_normal:GameImage, img_destacado:GameImage):
        self.normal = img_normal
        self.destacado = img_destacado
        self.is_normal = True
        self.x = 0
        self.y = 0
        self.width = img_normal.width
        self.heigth =img_normal.height

    def set_position(self, x, y):
        self.normal.set_position(x,y)
        self.destacado.set_position(x,y)
        self.x = x
        self.y = y

    def muda_estado(self, novo_estado:bool):
        self.is_normal = novo_estado

    def render(self):
        if self.is_normal:
            self.normal.draw()
        else:
            self.destacado.draw()
