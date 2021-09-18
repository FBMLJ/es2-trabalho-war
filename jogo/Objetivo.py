class Objetivo:
    def __init__(self) -> None:
        self.descricao = ""
        self.tipo = ""
        self.cor_a_destruir = ""
        self.continentes_a_conquistar = []  # lista de objetos do tipo continente
        self.territorios_a_conquistar_qtd = 0
        self.tropas_em_cada_territorios = 0

    def __eq__(self, other) -> bool:
        return self.descricao == other.descricao
