from unittest import TestCase
from jogo.Player import Player
from jogo.MatchStarter import MatchStarter
from jogo.TroopsManager import TroopsManager

class TestTroopsManager(TestCase):
    def test_recebimento_rodada_minimo(self):
        # Arrange
        match_starter = MatchStarter()
        troops_manager = TroopsManager()

        jogador = Player()

        lista_territorios = match_starter.inicia_territorios()
        lista_continentes = match_starter.inicia_continentes(lista_territorios)

        # Act
        troops_manager.recebimento_rodada(jogador, lista_continentes)

        #Assert
        self.assertEqual(3, jogador.tropas_pendentes)

    def test_recebimento_rodada_por_territorio(self):
        # Arrange
        match_starter = MatchStarter()
        troops_manager = TroopsManager()

        jogador = Player()

        lista_territorios = match_starter.inicia_territorios()
        lista_continentes = match_starter.inicia_continentes(lista_territorios)

        jogador.territorios.append(lista_territorios[0])
        jogador.territorios.append(lista_territorios[1])
        jogador.territorios.append(lista_territorios[2])
        jogador.territorios.append(lista_territorios[10])
        jogador.territorios.append(lista_territorios[11])
        jogador.territorios.append(lista_territorios[12])
        jogador.territorios.append(lista_territorios[20])
        jogador.territorios.append(lista_territorios[21])
        jogador.territorios.append(lista_territorios[22])
        jogador.territorios.append(lista_territorios[30])

        # Act
        troops_manager.recebimento_rodada(jogador, lista_continentes)

        # Assert
        self.assertEqual(5, jogador.tropas_pendentes)

    def test_recebimento_rodada_com_bonus_continente(self):
        # Arrange
        match_starter = MatchStarter()
        troops_manager = TroopsManager()

        jogador = Player()

        lista_territorios = match_starter.inicia_territorios()
        lista_continentes = match_starter.inicia_continentes(lista_territorios)

        for territorio in lista_territorios:
            if territorio.continente_nome == "Africa":
                jogador.territorios.append(territorio)

        # Act
        troops_manager.recebimento_rodada(jogador, lista_continentes)

        # Assert
        self.assertEqual(6, jogador.tropas_pendentes)

    def test_pode_movimentar(self):
        # Arrange
        match_starter = MatchStarter()
        troops_manager = TroopsManager()

        lista_territorios = match_starter.inicia_territorios()

        territorio_inicial = lista_territorios[0]
        territorio_inicial.quantidade_tropas = 4
        tropas_a_deslocar = 2
        territorio_inicial.tropas_deslocadas = 0
        territorio_final = lista_territorios[1]
        territorios = [territorio_final, territorio_inicial]

        # Act
        pode_deslocar = troops_manager.pode_movimentar(territorios, territorio_inicial,
                                                        territorio_final, tropas_a_deslocar)

        # Assert
        self.assertTrue(pode_deslocar)

    def test_verifica_tropas_a_movimentar_sucesso(self):
        # Arrange
        match_starter = MatchStarter()
        troops_manager = TroopsManager()

        lista_territorios = match_starter.inicia_territorios()

        territorio = lista_territorios[0]
        territorio.quantidade_tropas = 4
        tropas_a_deslocar = 2
        territorio.tropas_deslocadas = 0

        # Act
        pode_deslocar = troops_manager.verifica_tropas_a_movimentar(territorio, tropas_a_deslocar)

        # Assert
        self.assertTrue(pode_deslocar)

    def test_verifica_tropas_a_movimentar_falha(self):
        # Arrange
        match_starter = MatchStarter()
        troops_manager = TroopsManager()

        lista_territorios = match_starter.inicia_territorios()

        territorio = lista_territorios[0]
        territorio.quantidade_tropas = 4
        tropas_a_deslocar = 2
        territorio.tropas_deslocadas = 3

        # Act
        pode_deslocar = troops_manager.verifica_tropas_a_movimentar(territorio, tropas_a_deslocar)

        # Assert
        self.assertFalse(pode_deslocar)

    def test_verifica_se_territorios_sao_do_mesmo_jogador_sucesso(self):
        # Arrange
        match_starter = MatchStarter()
        troops_manager = TroopsManager()

        lista_territorios = match_starter.inicia_territorios()

        territorio_inicial = lista_territorios[0]
        territorio_final = lista_territorios[1]
        territorios = [territorio_final, territorio_inicial]

        # Act
        pode_deslocar = troops_manager.verifica_se_territorios_sao_do_mesmo_jogador(territorios, territorio_inicial, territorio_final)

        # Assert
        self.assertTrue(pode_deslocar)

    def test_verifica_se_territorios_sao_do_mesmo_jogador_falha(self):
        # Arrange
        match_starter = MatchStarter()
        troops_manager = TroopsManager()

        lista_territorios = match_starter.inicia_territorios()

        territorio_inicial = lista_territorios[0]
        territorio_dummy = lista_territorios[1]
        territorio_final = lista_territorios[2]
        territorios = [territorio_dummy, territorio_inicial]

        # Act
        pode_deslocar = troops_manager.verifica_se_territorios_sao_do_mesmo_jogador(territorios, territorio_inicial, territorio_final)

        # Assert
        self.assertFalse(pode_deslocar)

    def test_movimenta_tropas(self):
        # Arrange
        match_starter = MatchStarter()
        troops_manager = TroopsManager()

        lista_territorios = match_starter.inicia_territorios()

        territorio_inicial = lista_territorios[0]
        territorio_inicial.quantidade_tropas = 4
        tropas_a_deslocar = 2
        territorio_inicial.tropas_deslocadas = 0
        territorio_final = lista_territorios[1]
        territorio_final.quantidade_tropas = 1
        territorio_final.tropas_deslocadas = 0
        territorios = [territorio_final, territorio_inicial]

        # Act
        troops_manager.movimenta_tropas(territorios, territorio_inicial,
                                                       territorio_final, tropas_a_deslocar)

        # Assert
        territorio_destino_recebeu_tropas = territorio_final.quantidade_tropas == 3
        territorio_inicial_perdeu_tropas = territorio_inicial.quantidade_tropas == 2
        territorio_inicial_deslocou_tropas = territorio_final.tropas_deslocadas == 2
        self.assertTrue(territorio_destino_recebeu_tropas and territorio_inicial_perdeu_tropas and territorio_inicial_deslocou_tropas)
