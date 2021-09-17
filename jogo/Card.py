from PPlay.gameimage import GameImage

class Card:
    verso_img = "carta_verso.png"
    caminho_cartas = "assets/imagem/cartas/"
    
    def __init__(self, territorio: str, frente: str, fig: str, coringa: bool) -> None:
        self.territorio_nome = territorio
        self.frente = frente
        self.img = None
        self.img_select = None
        self.figura = fig
        self.coringa = coringa

    def __eq__(self, other):
        return self.territorio_nome == other.territorio_nome

    def carrega_imagem(self):
        self.img = GameImage(self.caminho_cartas + self.frente)
        self.img_select = GameImage(self.caminho_cartas + "card_select.png")
