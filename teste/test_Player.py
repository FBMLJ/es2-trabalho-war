from unittest import TestCase
from jogo.ObjectiveVerifier import ObjectiveVerifier
from jogo.MatchStarter import MatchStarter
from jogo.Player import Player

class TestPlayer(TestCase):
    def test_conquistou_continente(self):
        # Arrange
        objective_verifier = ObjectiveVerifier()
        match_starter = MatchStarter()

        lista_territorios = match_starter.inicia_territorios()
        lista_continentes = match_starter.inicia_continentes(lista_territorios)
        objetivos = objective_verifier.gera_objetivos(lista_continentes)

        nao_achou_objetivo_de_conquistar_continente = True
        posicao_na_lista = 0
        while nao_achou_objetivo_de_conquistar_continente:
            if len(objetivos[posicao_na_lista].continentes_a_conquistar) != 0:
                nao_achou_objetivo_de_conquistar_continente = False
                objetivo = objetivos[posicao_na_lista]
            posicao_na_lista += 1

        jogador_ganhador = Player()
        jogador_ganhador.objetivo = objetivo
        for continente in objetivo.continentes_a_conquistar:
            jogador_ganhador.territorios.extend(continente.territorios)

        # Act
        conquistou = jogador_ganhador.conquistou_continente(continente)

        # Assert
        self.assertTrue(conquistou)
