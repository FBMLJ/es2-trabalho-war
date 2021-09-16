from jogo.Continente import Continente
from jogo.Territorio import Territorio

class Player:
    def __init__(self) -> None:
        self.territorios = []
        self.cartas = []
        self.tropas_pendentes = 0
        self.objetivo = None
        self.pode_jogar = False
        self.cor = ""
        self.bot = False

    def conquistou_continente(self, continente:Continente) -> bool:
        territorios_do_continente = []
        # Busca os territorios do jogador que fazem parte daquele continente
        for territorio in self.territorios:
            if territorio.continente_nome == continente.nome:
                territorios_do_continente.append(territorio)
        # Se o jogador tiver todos os territorios do continente
        if len(territorios_do_continente) == len(continente.territorios):
            return True
        return False

    def possui_territorio(self, possivel_territorio:Territorio) -> bool:
        for territorio in self.territorios:
            if possivel_territorio == territorio:
                return True
        return False