from PPlay.gameimage import GameImage

class Card:
    verso_img = "carta_verso.png"
    caminho_cartas = "assets/imagem/cartas/"
    
    def __init__(self, territorio: str, frente: str, fig: str, coringa: bool) -> None:
        self.territorio_nome = territorio
        self.img = GameImage(self.caminho_cartas + frente)
        self.figura = fig
        self.coringa = coringa

    def __eq__(self, other):
        return self.territorio_nome == other.territorio_nome
