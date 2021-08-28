class Card:
    def __init__(self) -> None:
        self.territorio_nome = ""
        self.frente_img = ""
        self.verso_img = ""
        self.figura = ""
        self.coringa = False

    def __eq__(self, other):
        return self.territorio_nome == other.territorio_nome