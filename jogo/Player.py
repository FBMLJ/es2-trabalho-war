class Player:
    def __init__(self) -> None:
        self.territorios = []
        self.cartas = []
        self.tropas_pendentes = 0
        self.objetivo = None
        self.pode_jogar = False
        self.cor = ""