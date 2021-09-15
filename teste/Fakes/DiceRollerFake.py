class DiceRollerFake:
    def __init__(self, atacante_ganha:bool):
        self.atacante_ganha = atacante_ganha

    def rolar_dados_atacante(self) -> int:
        if self.atacante_ganha:
            return 6
        return 1

    def rolar_dados_defensor(self) -> int:
        if self.atacante_ganha:
            return 1
        return 6
