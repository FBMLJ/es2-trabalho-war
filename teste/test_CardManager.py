from unittest import TestCase
from jogo.CardManager import CardManager
from jogo.MatchStarter import MatchStarter
from jogo.Player import Player

class TestCardManager(TestCase):
    def test_inicia_cartas(self):
        # Arrange
        card_manager = CardManager()
        match_starter = MatchStarter()

        lista_territorios = match_starter.inicia_territorios()

        # Act
        lista_cartas = card_manager.inicia_cartas()

        # Assert
        coringas_qtd = 0
        cartas_de_territorios_qtd = 0
        for carta in lista_cartas:
            for territorio in lista_territorios:
                if carta.territorio_nome == territorio.nome:
                    cartas_de_territorios_qtd += 1
            if carta.coringa:
                coringas_qtd += 1
        cartas_distribuidas_corretamente = coringas_qtd == 2 and cartas_de_territorios_qtd == 42
        self.assertTrue(cartas_distribuidas_corretamente and len(lista_cartas) == 44)


    def test_troca_cartas(self):
        # Arrange
        card_manager = CardManager()
        match_starter = MatchStarter()

        lista_territorios = match_starter.inicia_territorios()
        lista_cartas = card_manager.inicia_cartas()

        mao_do_jogador = [lista_cartas[2], lista_cartas[3], lista_cartas[4], lista_cartas[5], lista_cartas[6]]
        cartas_trocadas = [mao_do_jogador[0], mao_do_jogador[1], mao_do_jogador[2]]

        territorios = [lista_territorios[0], lista_territorios[1]]
        territorios[0].quantidade_tropas = 0
        territorios[1].quantidade_tropas = 0

        # Act
        bonus_troca = card_manager.troca_cartas(mao_do_jogador, cartas_trocadas, territorios)

        # Assert
        tirou_cartas_da_mao = len(mao_do_jogador) == 2
        bonus_territorio = territorios[0].quantidade_tropas == 2 and territorios[1].quantidade_tropas == 2
        bonus_correto = bonus_troca == 4
        bonus_atualizado = card_manager.bonus_de_troca == 6
        self.assertTrue(bonus_correto and tirou_cartas_da_mao and bonus_territorio and bonus_atualizado)

    def test_deve_trocar_sucesso(self):
        # Arrange
        card_manager = CardManager()

        lista_cartas = card_manager.inicia_cartas()
        mao_do_jogador = [lista_cartas[2], lista_cartas[3], lista_cartas[4], lista_cartas[5], lista_cartas[6]]

        # Act
        deve_trocar = card_manager.deve_trocar(len(mao_do_jogador))

        # Assert
        self.assertTrue(deve_trocar)

    def test_deve_trocar_falha(self):
        # Arrange
        card_manager = CardManager()

        lista_cartas = card_manager.inicia_cartas()
        mao_do_jogador = [lista_cartas[3], lista_cartas[4], lista_cartas[5], lista_cartas[6]]

        # Act
        deve_trocar = card_manager.deve_trocar(len(mao_do_jogador))

        # Assert
        self.assertFalse(deve_trocar)

    def test_pode_trocar_iguais(self):
        # Arrange
        card_manager = CardManager()

        lista_cartas = card_manager.inicia_cartas()

        cartas_a_trocar = [lista_cartas[2], lista_cartas[5], lista_cartas[8]]

        # Act
        pode_trocar = card_manager.pode_trocar(cartas_a_trocar)

        # Assert
        self.assertTrue(pode_trocar)

    def test_pode_trocar_diferentes(self):
        # Arrange
        card_manager = CardManager()

        lista_cartas = card_manager.inicia_cartas()
        cartas_a_trocar = [lista_cartas[2], lista_cartas[3], lista_cartas[4]]

        # Act
        pode_trocar = card_manager.pode_trocar(cartas_a_trocar)

        # Assert
        self.assertTrue(pode_trocar)

    def test_pode_trocar_coringa(self):
        # Arrange
        card_manager = CardManager()

        lista_cartas = card_manager.inicia_cartas()
        cartas_a_trocar = [lista_cartas[0], lista_cartas[1], lista_cartas[2]]

        # Act
        pode_trocar = card_manager.pode_trocar(cartas_a_trocar)

        # Assert
        self.assertTrue(pode_trocar)

    def test_pode_trocar_falha(self):
        # Arrange
        card_manager = CardManager()

        lista_cartas = card_manager.inicia_cartas()
        cartas_a_trocar = [lista_cartas[2], lista_cartas[3], lista_cartas[5]]

        # Act
        pode_trocar = card_manager.pode_trocar(cartas_a_trocar)

        # Assert
        self.assertFalse(pode_trocar)

    def test_recebe_uma_carta(self):
        # Arrange
        card_manager = CardManager()

        lista_cartas = card_manager.inicia_cartas()
        cartas_na_mao = [lista_cartas[2], lista_cartas[3], lista_cartas[5]]
        jogador = Player()
        jogador.cartas = cartas_na_mao

        # Act
        card_manager.recebe_uma_carta(jogador)

        # Assert
        recebeu_uma_carta = len(jogador.cartas) == 4
        recebeu_carta_correta = jogador.cartas[3].territorio_nome == "Australia Ocidental"
        self.assertTrue(recebeu_uma_carta and recebeu_carta_correta)
