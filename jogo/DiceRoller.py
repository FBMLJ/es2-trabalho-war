import random


class DiceRoller:

    def rolar_dados_atacante(self) -> int:
        return random.randint(1, 6)

    def rolar_dados_defensor(self) -> int:
        return random.randint(1, 6)
