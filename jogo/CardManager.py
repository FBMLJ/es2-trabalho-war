from jogo.Bots.BotGeral import BotGeral
from jogo.Player import Player
from jogo.Card import Card
from constant import *
from random import shuffle

'''
Classe responsavel por gerenciar tudo relacionado ao uso de cartas
'''

class CardManager:
    def __init__(self) -> None:
        self.bonus_de_troca = 4
        self.cartas_no_monte = []
    
    '''
    Funcao que inicializa o baralho de cartas, com base no dicionario em constant.py
    '''
    def inicia_cartas(self):
        lista_de_cartas = []
        # Coringas
        lista_de_cartas.append(Card(None, "coringa.png", None, True))
        lista_de_cartas.append(Card(None, "coringa.png", None, True))
        for id_territorio in dicionario_territorios:
            nome_territorio = dicionario_territorios[id_territorio]
            imagem = str(id_territorio) + "_card.png"
            figura = dicionario_figura_territorio[id_territorio]
            lista_de_cartas.append(Card(nome_territorio, imagem, figura, False))
        if AMBIENTE != "TEST":
            shuffle(lista_de_cartas)
        # Atualizo o baralho
        self.cartas_no_monte = lista_de_cartas
        return lista_de_cartas

    '''
    Funcao que carrega as imagens das cartas
    '''
    def carrega_imagens(self):
        for carta in self.cartas_no_monte:
            carta.carrega_imagem()

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
            self.cartas_no_monte.append(cartas_trocadas[i])
        shuffle(self.cartas_no_monte)

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
    Se a quantidade de cartas a trocar for diferente de 3, proibe a troca
    Se existir um coringa, as cartas estao aptas para troca
    Se todas as cartas tiverem figuras iguais, permite a troca
    Se todas as cartas tiverem figuras diferentes, permite a troca
    Em todos os outros casos, proibe a troca
    '''
    def pode_trocar(self, cartas: list) -> bool:
        if len(cartas) != 3:
            return False
        for carta in cartas:
            if carta.coringa:
                return True
        if cartas[0].figura == cartas[1].figura == cartas[2].figura:
            return True
        if cartas[0].figura != cartas[1].figura != cartas[2].figura and cartas[0].figura != cartas[2].figura:
            return True
        return False

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