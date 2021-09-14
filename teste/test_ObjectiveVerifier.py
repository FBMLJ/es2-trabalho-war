from unittest import TestCase
from jogo.ObjectiveVerifier import ObjectiveVerifier
from jogo.Player import Player

class TestObjectiveVerifier(TestCase):
    def test_filtrar(self):
        #Arrange
        objective_verifier = ObjectiveVerifier()
        jogador_um = Player()
        jogador_um.cor = "AZUL"
        jogador_dois = Player()
        jogador_dois.cor = "VERDE"
        jogador_tres = Player()
        jogador_tres.cor = "VERMELHO"
        jogadores = [jogador_um, jogador_dois, jogador_tres]

        objetivos = []

        #Act
        objetivos_filtrados = objective_verifier.filtrar(objetivos, jogadores)

        #Assert
        cores_faltantes_nao_estao_presente = True
        self.assertTrue(cores_faltantes_nao_estao_presente)

    def test_verifica_objetivos(self):
        self.fail()

    def test_verificar_destruiu_cor(self):
        self.fail()

    def test_verifica_conquista_continentes(self):
        self.fail()

    def test_verifica_territorios_com_tropas(self):
        self.fail()
