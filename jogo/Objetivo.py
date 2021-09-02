class Objetivo:
    def __init__(self) -> None:
        self.descricao = ""
        self.tipo = ""
        self.cor_a_destruir = ""

    def __eq__(self, other) -> bool:
        return self.descricao == other.descricao