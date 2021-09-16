from unittest import TestCase
from jogo.ObjectiveVerifier import ObjectiveVerifier
from jogo.Player import Player
from jogo.Objetivo import Objetivo
from jogo.Continente import Continente
from jogo.Territorio import Territorio
from jogo.MatchStarter import MatchStarter

class TestObjectiveVerifier(TestCase):
    def test_filtrar(self):
        # Arrange
        objective_verifier = ObjectiveVerifier()
        match_starter = MatchStarter()

        jogador_um = Player()
        jogador_um.cor = "azul"
        jogador_dois = Player()
        jogador_dois.cor = "amarelo"
        jogador_tres = Player()
        jogador_tres.cor = "branco"
        jogadores = [jogador_um, jogador_dois, jogador_tres]

        lista_territorios = match_starter.inicia_territorios()
        lista_continentes = match_starter.inicia_continentes(lista_territorios)
        objetivos = objective_verifier.gera_objetivos(lista_continentes)
        
        # Act
        objetivos_filtrados = objective_verifier.filtrar(objetivos, jogadores)

        # Assert
        cores_filtradas = []
        for objetivo in objetivos_filtrados:
            if objetivo.cor_a_destruir != "":
                cores_filtradas.append(objetivo.cor_a_destruir)
        cores_faltantes_nao_estao_presentes = ("preto" not in cores_filtradas) and ("verde" not in cores_filtradas) and ("vermelho" not in cores_filtradas)
        self.assertTrue(cores_faltantes_nao_estao_presentes)

    def test_verificar_destruiu_cor(self):
        #Arrange
        objective_verifier = ObjectiveVerifier()
        match_starter = MatchStarter()

        lista_territorios = match_starter.inicia_territorios()
        lista_continentes = match_starter.inicia_continentes(lista_territorios)
        objetivos = objective_verifier.gera_objetivos(lista_continentes)

        jogador_ganhador = Player()
        jogador_ganhador.cor = "verde"
        jogador_perdedor = Player()
        jogador_perdedor.cor = "azul"

        nao_achou_objetivo_de_destruir_cor = True
        posicao_na_lista = 0
        while nao_achou_objetivo_de_destruir_cor:
            if objetivos[posicao_na_lista].cor_a_destruir == jogador_perdedor.cor:
                nao_achou_objetivo_de_destruir_cor = False
                objetivo = objetivos[posicao_na_lista]
            posicao_na_lista += 1

        jogador_ganhador.objetivo = objetivo
        for i in range(10):
            jogador_ganhador.territorios.append(lista_territorios[i])
        jogador_perdedor.territorios = []

        jogadores = [jogador_ganhador, jogador_perdedor]

        #Act
        ganhou = objective_verifier.verificar_destruiu_cor(jogador_ganhador, jogadores)

        #Assert
        self.assertTrue(ganhou)

    def test_verifica_conquista_continentes(self):
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
        ganhou = objective_verifier.verifica_conquista_continentes(jogador_ganhador)

        # Assert
        self.assertTrue(ganhou)

    def test_verifica_territorios_com_tropas(self):
        # Arrange
        objective_verifier = ObjectiveVerifier()
        match_starter = MatchStarter()

        lista_territorios = match_starter.inicia_territorios()
        lista_continentes = match_starter.inicia_continentes(lista_territorios)
        objetivos = objective_verifier.gera_objetivos(lista_continentes)

        nao_achou_objetivo_de_conquistar_territorios = True
        posicao_na_lista = 0
        while nao_achou_objetivo_de_conquistar_territorios:
            if objetivos[posicao_na_lista].territorios_a_conquistar_qtd > 0:
                nao_achou_objetivo_de_conquistar_territorios = False
                objetivo = objetivos[posicao_na_lista]
            posicao_na_lista += 1

        jogador_ganhador = Player()
        jogador_ganhador.objetivo = objetivo
        for i in range(objetivo.territorios_a_conquistar_qtd):
            lista_territorios[i].recebe_tropas(objetivo.tropas_em_cada_territorios)
            jogador_ganhador.territorios.append(lista_territorios[i])

        # Act
        ganhou = objective_verifier.verifica_territorios_com_tropas(jogador_ganhador)

        # Assert
        self.assertTrue(ganhou)
