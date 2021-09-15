from jogo.Bots.BotGeral import BotGeral
from jogo.Territorio import Territorio
from jogo.DiceRoller import DiceRoller

class CombateManager:

    def __init__(self, rolador_de_dados=DiceRoller()):
        self.rolador_de_dados = rolador_de_dados

    '''
    A funcao que realiza os ataques de um territoro a outro.
    Primeiro ela decide quantos dados cada jogador vai usar,
    Depois ela rola os dados para cada jogador,
    Depois ela compara os dados em ordem decrescente,
    Depois ela subtrai as tropas derrotadas,
    Depois verifica se houve conquista, se sim, opera a conquista sob o territorio
    Retorna as tropas sobreviventes do ataque
    '''
    def atacar(self, territorios_atacante: list, territorios_defensor: list,
    atacante: Territorio, defensor: Territorio, tropas_de_ataque = -1):
        # Quantos dados cada jogador vai usar
        if tropas_de_ataque != -1: # Se o jogador especificou quantas tropas que usar no ataque
            dados_atacantes = tropas_de_ataque
        else: # Se nao especificou quantas tropas usar
            if atacante.quantidade_tropas > 3:
                dados_atacantes = 3
            else:
                dados_atacantes = atacante.quantidade_tropas - 1
        if defensor.quantidade_tropas > 2:
            dados_defensores = 3
        else:
            dados_defensores = defensor.quantidade_tropas
        # Rola os dados para cada jogador
        rolagens_ataque = []
        rolagens_defesa = []

        dados_a_rolar = min(dados_atacantes, dados_defensores)
        for _ in range(dados_a_rolar):
            rolagens_ataque.append(self.rolador_de_dados.rolar_dados_atacante())
            rolagens_defesa.append(self.rolador_de_dados.rolar_dados_defensor())
        # Compara os dados em ordem decrescente
        vitorias_ataque = 0
        vitorias_defesa = 0
        rolagens_ataque.sort(reverse=True)
        rolagens_defesa.sort(reverse=True)
        for i in range(dados_a_rolar):
            if rolagens_ataque[i] > rolagens_defesa[i]:
                vitorias_ataque += 1
            else:
                vitorias_defesa += 1

        # Subtrai as tropas derrotadas
        atacante.perde_tropas(vitorias_defesa)
        defensor.perde_tropas(vitorias_ataque)

        sobreviventes = vitorias_ataque

        # Verifica se houve conquista
        if self.verifica_conquista(sobreviventes, defensor):
            self.conquista(territorios_atacante, territorios_defensor, atacante, defensor, sobreviventes)

        # Retorna as tropas sobreviventes do ataque
        #return sobreviventes #  retorno redundante, a funcao de conquista ja trata as tropas

    '''
    Funcao que checa se o atacante pode atacar o defensor
    Verifica se o atacante tem mais de dois exercitos
    Verifica se os territorios fazem fronteira
    '''
    def pode_atacar(self, atacante: Territorio, defensor: Territorio) -> bool:
        #Verifica se o atacante tem mais de dois exercitos
        if atacante.quantidade_tropas < 2:
            return False
        #Verifica de os territorios fazem fronteira
        return atacante.eh_vizinho(defensor)
    
    '''
    Funcao para validar quantidade de tropas atacantes escolhida pelo jogador
    Deve ser menor do que a quantidade de tropas no territorio atacante
    Nao pode ser menor do que 1
    '''
    def valida_qtd_tropas_atacantes(self, atacante: Territorio, tropas: int) -> bool:
        if tropas < 1:
            return False
        if tropas < atacante.quantidade_tropas:
            return True
        return False

    '''
    Funcao que opera a conquista de territorio
    O territorio conquistado vai para a lista de territorios do atacante
    Apenas as tropas vitoriosas na batalha podem ocupar o territorio
    O territorio conquistado sai da lista de territorios do defensor
    '''
    def conquista(self, territorios_atacante: list, territorios_defensor: list,
    atacante: Territorio, defensor: Territorio, sobreviventes: int) -> None:
        # O territorio conquistado vai para a lista de territorios do atacante
        territorios_atacante.append(defensor)
        # Apenas as tropas vitoriosas na batalha podem ocupar o territorio
        atacante.perde_tropas(sobreviventes)
        defensor.recebe_tropas(sobreviventes)
        # O territorio conquistado sai da lista de territorios do defensor
        territorios_defensor.remove(defensor)

    '''
    Funcao que verifica se houve a conquista apos o ataque
    '''
    def verifica_conquista(self, sobreviventes_ataque: int, defensor: Territorio) -> bool:
        return defensor.quantidade_tropas < 1 and sobreviventes_ataque > 0

    '''
    Funcao que itera pelos territorios para atacar do bot
    Itera pela lista de ataques do bot
    Verifica se o ataque pode acontecer
    Busca pelo jogador dono do territorio defensor
    Realiza o ataque
    '''
    def ataques_do_bot(self, bot: BotGeral, jogadores: list) -> None:
        #Itera pela lista de ataques do bot
        for i in range(bot.ataques_a_fazer):
            #Verifica se o ataque pode acontecer
            if self.pode_atacar(bot.ataques_a_fazer[i][0], bot.ataques_a_fazer[i][1]):
                #Busca pelo jogador dono do territorio defensor
                for jogador in jogadores:
                    for territorio in jogador.territorios:
                        if territorio.nome == bot.ataques_a_fazer[i][1].nome:
                            defensor = jogador
                #Realiza o ataque
                self.atacar(bot.territorios, defensor.territorios, bot.ataques_a_fazer[i][0], bot.ataques_a_fazer[i][1])
        return
