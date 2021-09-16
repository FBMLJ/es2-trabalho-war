from unittest import TestCase
from jogo.ObjectiveVerifier import ObjectiveVerifier
from jogo.MatchStarter import MatchStarter
from jogo.CombateManager import CombateManager
from teste.Fakes.DiceRollerFake import DiceRollerFake


class TestCombateManager(TestCase):
    def test_atacar_com_conquista(self):
        # Arrange
        match_starter = MatchStarter()
        atacante_vence = True
        rolador_de_dados_fake = DiceRollerFake(atacante_vence)
        combate_manager = CombateManager(rolador_de_dados_fake)

        lista_territorios = match_starter.inicia_territorios()

        atacante = lista_territorios[0]
        atacante.quantidade_tropas = 4
        defensor = lista_territorios[1]
        defensor.quantidade_tropas = 1

        territorio_atacante_dois = lista_territorios[10]
        territorio_atacante_tres = lista_territorios[9]
        territorio_defensor_dois = lista_territorios[8]
        territorio_defensor_tres = lista_territorios[7]

        territorios_atacante = [atacante, territorio_atacante_dois, territorio_atacante_tres]
        territorios_defensor = [defensor, territorio_defensor_dois, territorio_defensor_tres]

        # Act
        combate_manager.atacar(territorios_atacante, territorios_defensor, atacante, defensor)

        # Assert
        conquistou = len(territorios_atacante) == 4 and len(territorios_defensor) == 2
        moveu_tropas_corretamente = atacante.quantidade_tropas == 3 and defensor.quantidade_tropas == 1
        self.assertTrue(conquistou and moveu_tropas_corretamente)

    def test_atacar_defesa_ganha(self):
        # Arrange
        match_starter = MatchStarter()
        atacante_vence = False
        rolador_de_dados_fake = DiceRollerFake(atacante_vence)
        combate_manager = CombateManager(rolador_de_dados_fake)

        lista_territorios = match_starter.inicia_territorios()

        atacante = lista_territorios[0]
        atacante.quantidade_tropas = 4
        defensor = lista_territorios[1]
        defensor.quantidade_tropas = 3

        territorio_atacante_dois = lista_territorios[10]
        territorio_atacante_tres = lista_territorios[9]
        territorio_defensor_dois = lista_territorios[8]
        territorio_defensor_tres = lista_territorios[7]

        territorios_atacante = [atacante, territorio_atacante_dois, territorio_atacante_tres]
        territorios_defensor = [defensor, territorio_defensor_dois, territorio_defensor_tres]

        # Act
        combate_manager.atacar(territorios_atacante, territorios_defensor, atacante, defensor)

        # Assert
        nao_conquistou = len(territorios_atacante) == 3 and len(territorios_defensor) == 3
        manteve_as_tropas = atacante.quantidade_tropas == 1 and defensor.quantidade_tropas == 3
        self.assertTrue(nao_conquistou and manteve_as_tropas)

    def test_atacar_ataque_ganha_sem_conquista(self):
        # Arrange
        match_starter = MatchStarter()
        atacante_vence = True
        rolador_de_dados_fake = DiceRollerFake(atacante_vence)
        combate_manager = CombateManager(rolador_de_dados_fake)

        lista_territorios = match_starter.inicia_territorios()

        atacante = lista_territorios[0]
        atacante.quantidade_tropas = 3
        defensor = lista_territorios[1]
        defensor.quantidade_tropas = 5

        territorio_atacante_dois = lista_territorios[10]
        territorio_atacante_tres = lista_territorios[9]
        territorio_defensor_dois = lista_territorios[8]
        territorio_defensor_tres = lista_territorios[7]

        territorios_atacante = [atacante, territorio_atacante_dois, territorio_atacante_tres]
        territorios_defensor = [defensor, territorio_defensor_dois, territorio_defensor_tres]

        # Act
        combate_manager.atacar(territorios_atacante, territorios_defensor, atacante, defensor)

        # Assert
        nao_conquistou = len(territorios_atacante) == 3 and len(territorios_defensor) == 3
        manteve_as_tropas = atacante.quantidade_tropas == 3 and defensor.quantidade_tropas == 3
        self.assertTrue(nao_conquistou and manteve_as_tropas)

    def test_pode_atacar_tem_tropas_suficientes_e_faz_fronteira(self):
        # Arrange
        match_starter = MatchStarter()
        combate_manager = CombateManager()

        lista_territorios = match_starter.inicia_territorios()

        atacante = lista_territorios[0]
        atacante.quantidade_tropas = 2
        defensor = lista_territorios[1]
        defensor.quantidade_tropas = 3

        # Act
        pode_atacar = combate_manager.pode_atacar(atacante, defensor)

        #Assert
        self.assertTrue(pode_atacar)

    def test_pode_atacar_nao_tem_tropas_suficientes(self):
        # Arrange
        match_starter = MatchStarter()
        combate_manager = CombateManager()

        lista_territorios = match_starter.inicia_territorios()

        atacante = lista_territorios[0]
        atacante.quantidade_tropas = 1
        defensor = lista_territorios[1]
        defensor.quantidade_tropas = 3

        # Act
        pode_atacar = combate_manager.pode_atacar(atacante, defensor)

        # Assert
        self.assertFalse(pode_atacar)

    def test_pode_atacar_nao_esta_na_fronteira(self):
        # Arrange
        match_starter = MatchStarter()
        combate_manager = CombateManager()

        lista_territorios = match_starter.inicia_territorios()

        atacante = lista_territorios[0]
        atacante.quantidade_tropas = 3
        defensor = lista_territorios[30]
        defensor.quantidade_tropas = 3

        # Act
        pode_atacar = combate_manager.pode_atacar(atacante, defensor)

        # Assert
        self.assertFalse(pode_atacar)

    def test_valida_qtd_tropas_atacantes_sucesso(self):
        # Arrange
        match_starter = MatchStarter()
        combate_manager = CombateManager()

        lista_territorios = match_starter.inicia_territorios()

        atacante = lista_territorios[0]
        atacante.quantidade_tropas = 3
        quantidade_tropas = 2

        # Act
        pode_atacar = combate_manager.valida_qtd_tropas_atacantes(atacante, quantidade_tropas)

        # Assert
        self.assertTrue(pode_atacar)

    def test_valida_qtd_tropas_atacantes_falha(self):
        # Arrange
        match_starter = MatchStarter()
        combate_manager = CombateManager()

        lista_territorios = match_starter.inicia_territorios()

        atacante = lista_territorios[0]
        atacante.quantidade_tropas = 3
        quantidade_tropas = 3

        # Act
        pode_atacar = combate_manager.valida_qtd_tropas_atacantes(atacante, quantidade_tropas)

        # Assert
        self.assertFalse(pode_atacar)

    def test_conquista(self):
        # Arrange
        match_starter = MatchStarter()
        combate_manager = CombateManager()

        lista_territorios = match_starter.inicia_territorios()

        atacante = lista_territorios[0]
        atacante.quantidade_tropas = 4
        defensor = lista_territorios[1]
        defensor.quantidade_tropas = 0
        sobreviventes = 3

        territorio_atacante_dois = lista_territorios[10]
        territorio_atacante_tres = lista_territorios[9]
        territorio_defensor_dois = lista_territorios[8]
        territorio_defensor_tres = lista_territorios[7]

        territorios_atacante = [atacante, territorio_atacante_dois, territorio_atacante_tres]
        territorios_defensor = [defensor, territorio_defensor_dois, territorio_defensor_tres]

        # Act
        combate_manager.conquista(territorios_atacante, territorios_defensor, atacante, defensor, sobreviventes)

        # Assert
        conquistou = len(territorios_atacante) == 4 and len(territorios_defensor) == 2
        moveu_tropas_corretamente = atacante.quantidade_tropas == 1 and defensor.quantidade_tropas == 3
        self.assertTrue(conquistou and moveu_tropas_corretamente)

    def test_verifica_conquista_sucesso(self):
        # Arrange
        match_starter = MatchStarter()
        combate_manager = CombateManager()

        lista_territorios = match_starter.inicia_territorios()

        defensor = lista_territorios[1]
        defensor.quantidade_tropas = 0
        sobreviventes = 3

        # Act
        conquistou = combate_manager.verifica_conquista(sobreviventes, defensor)

        # Assert
        self.assertTrue(conquistou)

    def test_verifica_conquista_falha(self):
        # Arrange
        match_starter = MatchStarter()
        combate_manager = CombateManager()

        lista_territorios = match_starter.inicia_territorios()

        defensor = lista_territorios[1]
        defensor.quantidade_tropas = 1
        sobreviventes = 3

        # Act
        conquistou = combate_manager.verifica_conquista(sobreviventes, defensor)

        # Assert
        self.assertFalse(conquistou)
