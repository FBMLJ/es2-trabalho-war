from typing import List
from jogo.Territorio import *

class Continente:

    def __init__(self, nome, lista_territorios:List[Territorio], tropas_bonus):
        self.nome = nome
        self.territorios = lista_territorios
        self.bonus = tropas_bonus

    def continente_conquistado(self, cor_jogador):
        for territorio in self.territorios:
            if territorio.cor_tropas != cor_jogador:
                return False
        return True
