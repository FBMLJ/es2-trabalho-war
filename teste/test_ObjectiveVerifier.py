from unittest import TestCase
from jogo.ObjectiveVerifier import ObjectiveVerifier
from jogo.Player import Player
from jogo.Objetivo import Objetivo
from jogo.Continente import Continente
from jogo.Territorio import Territorio
from jogo.MatchStarter import MatchStarter

class TestObjectiveVerifier(TestCase):
    def test_filtrar(self):
        #Arrange
        objective_verifier = ObjectiveVerifier()
        match_starter = MatchStarter()

        jogador_um = Player()
        jogador_um.cor = "azul"
        jogador_dois = Player()
        jogador_dois.cor = "amarelo"
        jogador_tres = Player()
        jogador_tres.cor = "branco"
        jogadores = [jogador_um, jogador_dois, jogador_tres]
        ''''
        objetivo_um = Objetivo()
        objetivo_um.cor_a_destruir = "azul"
        objetivo_dois = Objetivo()
        objetivo_dois.cor_a_destruir = "amarelo"
        objetivo_tres = Objetivo()
        objetivo_tres.cor_a_destruir = "branco"
        objetivo_quatro = Objetivo()
        objetivo_quatro.cor_a_destruir = "preto"
        objetivo_cinco = Objetivo()
        objetivo_cinco.cor_a_destruir = "verde"
        objetivo_seis = Objetivo()
        objetivo_seis.cor_a_destruir = "vermelho"
        objetivo_sete = Objetivo()
        objetivo_sete.cor_a_destruir = ""
        objetivos = [objetivo_um, objetivo_dois, objetivo_tres, objetivo_quatro, objetivo_cinco, objetivo_seis, objetivo_sete]
        '''
        #Act
        objetivos_filtrados = objective_verifier.filtrar(objetivos, jogadores)

        #Assert
        cores_filtradas = []
        for objetivo in objetivos_filtrados:
            if objetivo.cor_a_destruir != "":
                cores_filtradas.append(objetivo.cor_a_destruir)
        cores_faltantes_nao_estao_presentes = ("preto" not in cores_filtradas) and ("verde" not in cores_filtradas) and ("vermelho" not in cores_filtradas)
        self.assertTrue(cores_faltantes_nao_estao_presentes)

    def test_verifica_objetivos(self):
        #Arrange
        #Act
        #Assert
        self.assertTrue(True)

    def test_verificar_destruiu_cor(self):
        #Arrange
        objective_verifier = ObjectiveVerifier()

        objetivo_ganhador = Objetivo()
        objetivo_ganhador.cor_a_destruir = "azul"
        jogador_ganhador = Player()
        jogador_ganhador.cor = "verde"
        jogador_ganhador.objetivo = objetivo_ganhador
        jogador_ganhador.territorios = [1, 2, 3, 4]

        objetivo_perdedor = Objetivo()
        objetivo_perdedor.cor_a_destruir = "verde"
        jogador_perdedor = Player()
        jogador_perdedor.cor = "azul"
        jogador_perdedor.territorios = []
        jogador_perdedor.objetivo = objetivo_perdedor
        jogadores = [jogador_ganhador, jogador_perdedor]

        #Act
        ganhou = objective_verifier.verificar_destruiu_cor(jogador_ganhador, jogadores)

        #Assert
        self.assertTrue(ganhou)

    def test_verifica_conquista_continentes(self):
        #Arrange
        objective_verifier = ObjectiveVerifier()

        territorio_um = Territorio()
        territorio_dois = Territorio()
        territorio_tres = Territorio()
        territorio_quatro = Territorio()
        territorio_cinco = Territorio()

        continente_um = Continente()
        continente_dois = Continente()
        objetivo = Objetivo()
        objetivo.continentes_a_conquistar = [continente_um, continente_dois]
        jogador = Player()

        #Act

        #Assert
        self.fail()

    def test_verifica_territorios_com_tropas(self):
        self.fail()
