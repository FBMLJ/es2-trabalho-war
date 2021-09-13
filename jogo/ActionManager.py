from jogo.Player import Player

class ActionManager:
    '''
    Objeto responsavel por organizar os turnos
    Responsavel por qual jogador deve jogar no turno atual
    Responsavel pela ordem das acoes do jogador
    '''
    def __init__(self, jogadores: list) -> None:
        self.jogadores_partida = jogadores
        self.index_jogador_do_turno = 0
        self.jogador_turno = self.jogadores_partida[self.index_jogador_do_turno]
        self.jogador_turno.pode_jogar = True
        self.hora_de_receber_tropas = False
        self.hora_de_colocar_tropas = False
        self.hora_de_atacar = False
        self.hora_de_deslocar_tropas = False
        self.hora_de_receber_carta = False

    '''
    Funcao que retorna o jogador do turno atual
    '''
    def retorna_jogador_do_turno_atual(self) -> Player:
        return self.jogador_turno

    '''
    Funcao para passar o turno
    Finaliza o turno do ultimo jogador
    Verifica qual o index do proximo jogador da lista de forma ciclica
    Atualiza o jogador do proximo turno
    '''
    def passar_turno(self) -> None:
        #Finaliza o turno do ultimo jogador
        self.jogador_turno.pode_jogar = False
        self.hora_de_receber_carta = False
        #Verifica qual o index do proximo jogador da lista de forma ciclica
        if self.index_jogador_do_turno < len(self.jogadores_partida)-1:
            self.index_jogador_do_turno += 1
        else:
            self.index_jogador_do_turno = 0
        #Atualiza o jogador do proximo turno
        self.jogador_turno = self.jogadores_partida[self.index_jogador_do_turno]
        self.jogador_turno.pode_jogar = True

    '''
    Funcoes que determinam qual acao deve ser tomada no momento
    1. Recebe tropas
    2. Coloca as tropas no mapa
    3. Ataca outros jogadores
    4. Desloca tropas
    5. Recebe cartas se ganhou algum territorio
    '''
    def comeca_turno(self) -> None:
        self.hora_de_receber_tropas = True

    def jogador_recebeu_tropas(self) -> None:
        self.hora_de_receber_tropas = False
        self.hora_de_colocar_tropas = True

    def jogador_colocou_tropas(self) -> None:
        self.hora_de_colocar_tropas = False
        self.hora_de_atacar = True

    def jogador_atacou(self) -> None:
        self.hora_de_atacar = False
        self.hora_de_deslocar_tropas = True

    def jogador_deslocou_tropas(self) -> None:
        self.hora_de_deslocar_tropas = False
        self.hora_de_receber_carta = True