class Card:
    verso_img = "carta_verso.png"

    def __init__(self, territorio: str, frente: str, fig: str, coringa: bool) -> None:
        self.territorio_nome = territorio
        self.frente_img = frente
        self.figura = fig
        self.coringa = coringa

    def __eq__(self, other):
        return self.territorio_nome == other.territorio_nome
