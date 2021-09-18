from unittest import TestCase
from jogo.MatchStarter import MatchStarter
from jogo.Territorio import Territorio

class TestTerritorio(TestCase):
    def test_perde_tropas_sucesso(self):
        # Arrange
        match_starter = MatchStarter()

        lista_territorios = match_starter.inicia_territorios()

        territorio = lista_territorios[0]
        territorio.quantidade_tropas = 8

        # Act
        territorio.perde_tropas(3)

        # Assert
        self.assertEqual(5, territorio.quantidade_tropas)

    def test_perde_tropas_falha(self):
        # Arrange
        match_starter = MatchStarter()

        lista_territorios = match_starter.inicia_territorios()

        territorio = lista_territorios[0]
        territorio.quantidade_tropas = 3

        # Act
        territorio.perde_tropas(5)

        # Assert
        self.assertEqual(3, territorio.quantidade_tropas)

    def test_recebe_tropas(self):
        # Arrange
        match_starter = MatchStarter()

        lista_territorios = match_starter.inicia_territorios()

        territorio = lista_territorios[0]
        territorio.quantidade_tropas = 3

        # Act
        territorio.recebe_tropas(5)

        # Assert
        self.assertEqual(8, territorio.quantidade_tropas)

    def test_esta_na_fronteira_sucesso(self):
        # Arrange
        match_starter = MatchStarter()

        lista_territorios = match_starter.inicia_territorios()

        territorio = lista_territorios[0]
        territorio_vizinho = lista_territorios[1]

        # Act
        esta_na_fronteira = territorio.esta_na_fronteira(territorio_vizinho)

        # Assert
        self.assertTrue(esta_na_fronteira)

    def test_esta_na_fronteira_falha(self):
        # Arrange
        match_starter = MatchStarter()

        lista_territorios = match_starter.inicia_territorios()

        territorio = lista_territorios[0]
        territorio_nao_vizinho = lista_territorios[30]

        # Act
        esta_na_fronteira = territorio.esta_na_fronteira(territorio_nao_vizinho)

        # Assert
        self.assertFalse(esta_na_fronteira)

    def test_fim_de_turno(self):
        # Arrange
        match_starter = MatchStarter()

        lista_territorios = match_starter.inicia_territorios()

        territorio = lista_territorios[0]
        territorio.tropas_deslocadas = 5

        # Act
        territorio.fim_de_turno()

        # Assert
        self.assertEqual(0, territorio.tropas_deslocadas)
