from jogo.Territorio import Territorio
from jogo.Player import Player

class TroopsManager:

    '''
    Funcao que entrega o bonus de tropa por rodada
    Recebimento padrao eh a parte inteira da metade de territorios possuidos
    O Recebimento padrao nao pode ser menor do que 3
    Caso haja um continente conquistado por completo, recebe o bonus do continente
    '''
    def recebimento_rodada(self, jogador: Player, continentes: list) -> None:
        # Recebimento padrao eh a parte inteira da metade de territorios possuidos
        recebimento_padrao = int(len(jogador.territorios)/2)
        # Mas nao pode ser menor do que 3
        if recebimento_padrao < 4:
            recebimento_padrao = 3
        jogador.tropas_pendentes += recebimento_padrao
        # Caso haja um continente conquistado por completo, recebe o bonus do continente
        for continente in continentes:
            if jogador.conquistou_continente(continente):
                jogador.tropas_pendentes += continente.bonus

    '''
    Funcao que verifica se pode deslocar tropas entre territorios
    Checa se os territorios fazem fronteira
    Checa se o valor escolhido de tropas a deslocar eh valido
    Checa se os territorios do deslocamento sao do mesmo jogador
    '''
    def pode_movimentar(self, territorios: list, territorio_inicial: Territorio, territorio_destino: Territorio, tropas_a_deslocar: int) -> bool:
        esta_na_fronteira = territorio_inicial.eh_vizinho(territorio_destino)
        tem_tropas_pra_movimentar = self.verifica_tropas_a_movimentar(territorio_inicial, tropas_a_deslocar)
        sao_do_mesmo_jogador = self.verifica_se_territorios_sao_do_mesmo_jogador(territorios, territorio_inicial, territorio_destino)
        #print("esta_na_fronteira {}\ntem_tropas_pra_movimentar {}\nsao_do_mesmo_jogador {}".format(esta_na_fronteira, tem_tropas_pra_movimentar, sao_do_mesmo_jogador))
        return esta_na_fronteira and tem_tropas_pra_movimentar and sao_do_mesmo_jogador

    '''
    Funcao que verifica se a quantidade de tropas a deslocar e valida
    Checa se ao deslocar as tropas, havera ainda 1 exercito ocupante
    Considera que tropas deslocadas no mesmo turno para o territorio inicial nao podem ser deslocadas de novo
    '''
    def verifica_tropas_a_movimentar(self, territorio_inicial: Territorio, tropas_a_deslocar: int) -> bool:
        return tropas_a_deslocar <= territorio_inicial.quantidade_tropas - territorio_inicial.tropas_deslocadas

    '''
    Funcao que verifica se os territorios do deslocamento sao do mesmo jogador
    '''
    def verifica_se_territorios_sao_do_mesmo_jogador(self, territorios: list, territorio_inicial: Territorio, territorio_destino: Territorio) -> bool:
        return territorio_inicial in territorios and territorio_destino in territorios

    '''
    Funcao que movimenta tropas entre territorios
    Territorio destino recebe tropas deslocadas
    Marca deslocamento de tropas no territorio destino
    Retira tropas do territorio inicial
    '''
    def movimenta_tropas(self, territorios: list, territorio_inicial: Territorio, territorio_destino: Territorio, tropas_a_deslocar: int) -> bool:
        if self.pode_movimentar(territorios, territorio_inicial, territorio_destino, tropas_a_deslocar):
            territorio_destino.recebe_tropas(tropas_a_deslocar)
            territorio_destino.tropas_deslocadas = tropas_a_deslocar
            territorio_inicial.perde_tropas(tropas_a_deslocar)
            return True
        else:
            return False
