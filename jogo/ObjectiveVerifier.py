from jogo.Player import Player
from jogo.Objetivo import Objetivo
from constant import *

class ObjectiveVerifier:
    def __init__(self) -> None:
        pass

    '''
    Funcao para filtrar os objetivos que sao de destruir jogadores que nao estao na partida
    Primeiro pega as cores dos jogadores na partida
    Depois adiciona os objetivos que nao envolvem destruir um jogador de cor faltante
    '''
    def filtrar(self, objetivos: list, jogadores: list) -> list:
        # Primeiro pega as cores dos jogadores na partida
        cores_dos_jogadores = []
        for jog in jogadores:
            cores_dos_jogadores.append(jog.cor)
        # Depois adiciona os objetivos que nao envolvem destruir um jogador de cor faltante
        objetivos_filtrados = []
        for obj in objetivos:
            if obj.cor_a_destruir in cores_dos_jogadores or obj.cor_a_destruir == "":
                objetivos_filtrados.append(obj)
        return objetivos_filtrados

    '''
    Funcao que verifica se algum jogador concluiu seu objetivo, retorna o jogador ganhador
    Se um jogador tiver o objetivo de destruir alguma cor
    Se um jogador tiver o objetivo de conquistar continentes especificos
    Se um jogador tiver o objetivo de conquistar X territorios com um minimo de Y tropas
    Se ninguem tiver ganhado, retorna Nulo
    '''
    def verifica_objetivos(self, jogadores: list) -> Player:
        ganhou = False
        for jogador in jogadores:
            # Se um jogador tiver o objetivo de destruir alguma cor
            if jogador.objetivo.cor_a_destruir != "":
                ganhou = self.verificar_destruiu_cor(jogador, jogadores)
                if ganhou:
                    return jogador
            # Se um jogador tiver o objetivo de conquistar continentes especificos
            if len(jogador.objetivo.continentes_a_conquistar) != 0:
                ganhou = self.verifica_conquista_continentes(jogador)
                if ganhou:
                    return jogador
            # Se um jogador tiver o objetivo de conquistar X territorios com um minimo de Y tropas
            if jogador.objetivo.territorios_a_conquistar_qtd > 0:
                ganhou = self.verifica_territorios_com_tropas(jogador)
                if ganhou:
                    return jogador
        # Se ninguem tiver ganhado, retorna Nulo
        return None

    '''
    Funcao que verifica se a cor a ser destruida ja foi destruida
    Itera pela lista de jogadores da partida
    Procura o jogador cuja cor deve ser destruida
    Se este jogador tiver 0 territoros, conta que ele foi destruido
    '''
    def verificar_destruiu_cor(self, jogador: Player, jogadores: list) -> bool:
        # Considera, a principio, que o objetivo nao foi atingido
        destruiu_pessimista = False
        # Itera pela lista de jogadores da partida
        for jog_itr in jogadores:
            # Se este jogador tiver 0 territoros e ele for da cor a ser destruida
            if len(jog_itr.territorios) == 0 and jog_itr.cor == jogador.objetivo.cor_a_destruir:
                destruiu_pessimista = True
        return destruiu_pessimista

    '''
    Funcao que verifica se os continentes foram conquistados pelo jogador
    Primeiro conta quantos continentes devem ser conquistados
    Depois Itera pelos continentes a serem conquistados
    Depois busca os territorios do jogador que fazem parte daquele continente
    Se o jogador tiver todos os territorios do coninente, entao e subtraido 1 un. da quantidade de continentes a conquistar
    Se nao sobrou continentes a conquistar, retorna Verdade
    Se sobrou, retorna Mentira
    '''
    def verifica_conquista_continentes(self, jogador: Player) -> bool:
        # Primeiro conta quantos continentes devem ser conquistados
        continentes_conquistados_qtd = len(jogador.objetivo.continentes_a_conquistar)
        # Depois Itera pelos continentes a serem conquistados
        for continente_a_verificar in jogador.objetivo.continentes_a_conquistar:
            # Se o jogador tiver todos os territorios do continente, entao e subtraido 1 un. da quantidade de continentes a conquistar
            if jogador.conquistou_continente(continente_a_verificar):
                continentes_conquistados_qtd -= 1
        # Se nao sobrou continentes a conquistar, retorna Verdade
        if continentes_conquistados_qtd == 0:
            return True
        # Se sobrou, retorna Mentira
        else:
            return False

    '''
    Funcao que verifica a conquista de territorios com um numero minimo de tropas em cada
    Primeiro verifica se o jogador tem o minimo de territorios necessario, se nao tiver retorna Mentira
    Depois verifica quantos territorios tem o minimo de tropas necessarias
    Se tiver territorios o suficiente com o minimo de tropas necessarias, retorna Verdade
    Se nao, retorna Mentira
    '''
    def verifica_territorios_com_tropas(self, jogador: Player) -> bool:
        # Primeiro verifica se o jogador tem o minimo de territorios necessario, se nao tiver retorna Mentira
        territorios_conquistados_qtd = len(jogador.territorios)
        if territorios_conquistados_qtd < jogador.objetivo.territorios_a_conquistar_qtd:
            return False
        # Depois verifica quantos territorios tem o minimo de tropas necessarias
        qts_territorios_tem_as_tropas_minimas = 0
        for territorio_itr in jogador.territorios:
            if territorio_itr.quantidade_tropas >= jogador.objetivo.tropas_em_cada_territorios:
                qts_territorios_tem_as_tropas_minimas += 1
        # Se tiver territorios o suficiente com o minimo de tropas necessarias, retorna Verdade
        if qts_territorios_tem_as_tropas_minimas >= jogador.objetivo.territorios_a_conquistar_qtd:
            return True
        # Se nao, retorna Mentira
        else:
            return False

    '''
    Funcao que gera todos os objetivos possíveis do jogo 
    e os armazena em uma lista para que possam ser distribuidos
    '''
    def gera_objetivos(self, lista_continentes):

        for continente in lista_continentes:
            
            if continente.nome == "Africa":
                africa = continente
            elif continente.nome == "America do Norte":
                america_do_norte = continente
            elif continente.nome == "America do Sul":
                america_do_sul = continente
            elif continente.nome == "Asia":
                asia = continente
            elif continente.nome == "Europa":
                europa = continente
            elif continente.nome == "Oceania":
                oceania = continente

        lista_de_objetivos = []

        # adiciona todos os objetivos de destruir cores
        for cor in cores:
            objetivo_atual = Objetivo()
            objetivo_atual.descricao = "Destruir a cor " + cor
            objetivo_atual.cor_a_destruir = cor
            lista_de_objetivos.append(objetivo_atual)

        # adiciona o objetivo de conquistar Europa + américa do sul
        objetivo_atual = Objetivo()
        objetivo_atual.descricao = "Conquistar a Europa e a América do Sul"
        objetivo_atual.continentes_a_conquistar.append(europa)
        objetivo_atual.continentes_a_conquistar.append(america_do_sul)
        lista_de_objetivos.append(objetivo_atual)

        # adiciona o objetivo de conquistar Oceania + Ásia
        objetivo_atual = Objetivo()
        objetivo_atual.descricao = "Conquistar a Oceania e a Ásia"
        objetivo_atual.continentes_a_conquistar.append(oceania)
        objetivo_atual.continentes_a_conquistar.append(asia)
        lista_de_objetivos.append(objetivo_atual)

        # adiciona o objetivo de conquistar América do Norte e África
        objetivo_atual = Objetivo()
        objetivo_atual.descricao = "Conquistar a América do Norte e a África"
        objetivo_atual.continentes_a_conquistar.append(america_do_norte)
        objetivo_atual.continentes_a_conquistar.append(africa)
        lista_de_objetivos.append(objetivo_atual)

        # adiciona o objetivo de conquistar América do Norte e Oceania
        objetivo_atual = Objetivo()
        objetivo_atual.descricao = "Conquistar a América do Norte e a Oceania"
        objetivo_atual.continentes_a_conquistar.append(america_do_norte)
        objetivo_atual.continentes_a_conquistar.append(oceania)
        lista_de_objetivos.append(objetivo_atual)

        # adiciona o objetivo de conquistar Ásia e América do Sul
        objetivo_atual = Objetivo()
        objetivo_atual.descricao = "Conquistar a Ásia e a América do Sul"
        objetivo_atual.continentes_a_conquistar.append(asia)
        objetivo_atual.continentes_a_conquistar.append(america_do_sul)
        lista_de_objetivos.append(objetivo_atual)

        # adiciona o objetivo de conquistar Ásia e África
        objetivo_atual = Objetivo()
        objetivo_atual.descricao = "Conquistar a Ásia e a África"
        objetivo_atual.continentes_a_conquistar.append(asia)
        objetivo_atual.continentes_a_conquistar.append(africa)
        lista_de_objetivos.append(objetivo_atual)

        # adiciona o objetivo de conquistar 18 territórios com no mínimo duas tropas em cada
        objetivo_atual = Objetivo()
        objetivo_atual.descricao = "Conquistar 18 Territórios com no mínimo 2 tropas em cada"
        objetivo_atual.territorios_a_conquistar_qtd = 18
        objetivo_atual.tropas_em_cada_territorios = 2
        lista_de_objetivos.append(objetivo_atual)

        # adiciona o objetivo de conquistar 24 territórios
        objetivo_atual = Objetivo()
        objetivo_atual.descricao = "Conquistar 24 Territórios"
        objetivo_atual.territorios_a_conquistar_qtd = 24
        objetivo_atual.tropas_em_cada_territorios = 1
        lista_de_objetivos.append(objetivo_atual)

        return lista_de_objetivos
