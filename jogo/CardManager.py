from jogo.Bots.BotGeral import BotGeral
from jogo.Player import Player
from jogo.Card import Card
from constant import *

'''
Classe responsavel por gerenciar tudo relacionado ao uso de cartas
'''

class CardManager:
    def __init__(self) -> None:
        self.bonus_de_troca = 4
        self.cartas_no_monte = 0
    
    '''
    Funcao que inicializa o baralho de cartas, exceto coringa, com base no dicionario em constant.py
    '''
    def inicia_cartas(self) -> list:
        lista_de_cartas = []
        # Coringas
        lista_de_cartas.append(Card(None, "coringa_carta.png", None, True))
        lista_de_cartas.append(Card(None, "coringa_carta.png", None, True))
        for id_territorio in dicionario_territorios:
            nome_territorio = dicionario_territorios[id_territorio]
            imagem = nome_territorio + "_carta.png"
            figura = dicionario_figura_territorio[id_territorio]
            lista_de_cartas.append(Card(nome_territorio, imagem, figura, False))
        #atualizo o tamanho do baralho
        self.cartas_no_monte = len(lista_de_cartas)
        return lista_de_cartas
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

    '''
    Funcao que troca as cartas do bot
    Chama a funcao trocar cartas para as cartas a serem trocadas
    Adiciona o bonus de tropas as tropas pendentes do bot
    '''
    def trocar_cartas_do_bot(self, bot: BotGeral) -> None:
        #Chama a funcao trocar cartas para as cartas a serem trocadas
        bonus = self.troca_cartas(bot.cartas, bot.cartas_a_trocar, bot.territorios)
        #Adiciona o bonus de tropas as tropas pendentes do bot
        bot.tropas_pendentes += bonus
        return