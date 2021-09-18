from unittest import TestCase
from jogo.Player import Player
from jogo.Continente import Continente
from jogo.MatchStarter import MatchStarter

class TestContinente(TestCase):
    def test_continente_conquistado(self):
        # Arrange
        match_starter = MatchStarter()

        jogador = Player()
        jogador.cor = "azul"

        lista_territorios = match_starter.inicia_territorios()
        lista_continentes = match_starter.inicia_continentes(lista_territorios)

        continente = lista_continentes[0]

        for territorio in continente.territorios:
            territorio.cor_tropas = jogador.cor
            jogador.territorios.append(territorio)

        # Act
        conquistou = continente.continente_conquistado("azul")

        # Assert
        self.assertTrue(conquistou)
