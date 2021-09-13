from jogo.Player import Player
from jogo.Card import Card

class CardManager:
    def __init__(self, cartas: list) -> None:
        self.bonus_de_troca = 4
        self.cartas_no_monte = cartas
    
    '''
    Funcao que retorna o bonus de tropas por troca
    Remove as cartas a serem trocadas da mao do jogador,
    Confere o bonus de tropa aos territorios conquistados
    Retorna o bonus de troca da rodada atual.
    '''
    def troca_cartas(self, mao_do_jogador: list, cartas_trocadas: list, territorios: list) -> int:
        # Remove as cartas a serem trocadas da mao do jogador
        for i in range(3):
            mao_do_jogador.remove(cartas_trocadas[i])

        #Confere o bonus de tropa aos territorios conquistados
        for territorio in territorios:
            for carta in cartas_trocadas:
                if territorio.nome == carta.territorio_nome:
                    territorio.recebe_tropas(2)
        
        #Retorna o bonus de troca da rodada atual
        tropas_a_receber = self.bonus_de_troca
        self.bonus_de_troca += 2
        return tropas_a_receber

    '''
    Funcao que retorna se o jogador deve ou nao trocar cartas naquele turno
    '''
    def deve_trocar(self, num_cartas: int) -> bool:
        if num_cartas >= 5:
            return True
        else:
            return False

    '''
    Funcao que retorna se a lista de cartas esta apta para troca ou nao
    Algoritmo otimista
    Considera a principio que todas as cartas sao iguais, e busca a diferente
    Considera a principio que todas as cartas sao diferentes, e busca uma igual
    '''
    def pode_trocar(self, cartas: list) -> bool:
        iguais_otimismo = True
        diferente_otimismo = True
        for i in range(2):
            if cartas[i].figura != cartas[i+1].figura and not (cartas[i].coringa or cartas[i+1].coringa):
                iguais_otimismo = False
            if cartas[i].figura == cartas[i+1].figura and not (cartas[i].coringa or cartas[i+1].coringa):
                diferente_otimismo = False

        return iguais_otimismo or diferente_otimismo

    '''
    Funcao que tira uma carta do topo do monte e da para o jogador
    '''
    def recebe_uma_carta(self, jogador: Player) -> None:
        jogador.cartas.append(self.cartas_no_monte.pop())