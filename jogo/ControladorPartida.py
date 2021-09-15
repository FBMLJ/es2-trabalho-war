from jogo.Territorio import Territorio
from PPlay.window import Window
from PPlay.gameimage import GameImage
from PPlay.mouse import Mouse
from jogo.ControladorMapa import ControladorMapa
from jogo.MatchStarter import MatchStarter
from jogo.Objetivo import *
from jogo.Card import Card
from jogo.Player import Player
from jogo.CardManager import CardManager
from jogo.ObjectiveVerifier import ObjectiveVerifier
from jogo.TroopsManager import TroopsManager
from componentes.hudTurno import hudTurno
from componentes.hudSelecionaTropas import HudSelecionaTropas
from componentes.hudCombate import HudCombate
from constant import *

class ControladorPartida:
    caminho_hud = "assets/imagem/hud/"

    def __init__(self, janela:Window, jogadores: list):
        self.iniciador_de_partida = MatchStarter()
        self.gerenciador_mapa = ControladorMapa(janela)
        self.gerenciador_mapa.lista_territorios = self.iniciador_de_partida.inicia_territorios()
        self.gerenciador_mapa.set_lista_continentes(self.iniciador_de_partida.inicia_continentes(self.gerenciador_mapa.lista_territorios))
        self.gerenciador_mapa.carrega_imagens_dos_territorios()
        self.gerenciador_cartas = CardManager()
        self.gerenciador_objetivos = ObjectiveVerifier()
        self.gerenciador_tropas = TroopsManager()
        self.jogadores = jogadores
        self.todos_os_objetivos = self.gerenciador_objetivos.gera_objetivos(self.gerenciador_mapa.lista_continentes)        

        self.iniciador_de_partida.distribui_cores(self.jogadores)
        self.iniciador_de_partida.distribui_territorios(self.gerenciador_mapa.lista_territorios, self.jogadores)
        self.iniciador_de_partida.distribui_objetivos(self.todos_os_objetivos, self.jogadores)
            
        self.hud_turno = hudTurno(janela)
        self.hud_seleciona_quantidade = HudSelecionaTropas(janela)
        self.hud_combate = HudCombate(janela)
        self.janela = janela
        self.mouse = Mouse()
        self.jogador_vencedor = None
        self.baralho = []
        self.etapa_turno = 0
        self.rodada = 1

    def loop(self):
        self.janela.clear()

        #game loop
        while self.jogador_vencedor == None:  #Condicional para checar se algum objetivo foi alcancado
            for jogador in self.jogadores:
                self.jogador_vencedor = self.gerenciador_objetivos.verifica_objetivos(self.jogadores)
                if self.jogador_vencedor:
                    break
                '''
                Etapa 1 do turno: Distribuicao de exercitos
                '''
                self.etapa_turno = 1
                #self.distribuicao_exercitos(jogador)
                    
                if(self.rodada > 1): #Na primeira rodada so ha distribuicao de exercitos
                    
                    '''
                    Etapa 2 do turno: Combate
                    '''
                    self.etapa_turno = 2
                    finalizar_turno = self.combate(jogador)
                    '''
                    Etapa 3 do turno: Movimentacao de exercitos
                    '''
                    self.etapa_turno = 3
                    if not finalizar_turno:
                        self.movimentacao_exercitos(jogador)

                self.render()
                self.janela.update()
            self.rodada += 1

    def render(self):
        self.gerenciador_mapa.render(self.etapa_turno)
        self.hud_turno.render()
        if len(self.gerenciador_mapa.territorios_selecionados) > 0 and self.etapa_turno == 1:
            self.hud_seleciona_quantidade.render() #  A hud so eh exibida se houver territorio selecionado na etapa de distribuicao
        if(self.etapa_turno == 2):
            self.hud_combate.render()

    def inicia_cartas(self) -> None:
        for id_territorio in dicionario_territorios:
            nome_territorio = dicionario_territorios[id_territorio]
            imagem = nome_territorio + "_carta.png"
            figura = dicionario_figura_territorio[id_territorio]
            self.todas_as_cartas.append(Card(nome_territorio, imagem, figura, False))

    def distribuicao_exercitos(self, jogador:Player) -> None:
        self.hud_turno.icone_distribuir.is_normal = False #  Destacando o icone da etapa de distribuicao de tropas

        self.gerenciador_tropas.recebimento_rodada(jogador, self.gerenciador_mapa.lista_continentes)
        self.hud_seleciona_quantidade.maximo = jogador.tropas_pendentes #  Quantidade de tropas a ser distribuida
        self.gerenciador_mapa.territorios_selecionados = []
        etapa_concluida = False
        while not etapa_concluida:
            self.gerenciador_mapa.selecionar_territorio(self.mouse, jogador)
            clicou_ok = self.hud_seleciona_quantidade.update(self.mouse)
            if clicou_ok: #  Apos clicar no OK, termina de distribuir tropas para o territorio selecionado
                tropas_distribuidas = self.hud_seleciona_quantidade.quantidade
                self.gerenciador_mapa.territorios_selecionados[0].quantidade_tropas += tropas_distribuidas
                jogador.tropas_pendentes -= tropas_distribuidas
                self.hud_seleciona_quantidade.maximo = jogador.tropas_pendentes
                self.hud_seleciona_quantidade.quantidade = 0
                self.hud_seleciona_quantidade.caixa_quantidade.texto = "0"
                self.gerenciador_mapa.pode_desenhar = True 
                self.gerenciador_mapa.limpa_territorios_selecionados()

            if jogador.tropas_pendentes == 0:
                etapa_concluida = True
            
            self.render()
            self.janela.update()
        
        self.gerenciador_mapa.limpa_territorios_selecionados()
        self.hud_turno.icone_distribuir.is_normal = True

    def combate(self, jogador) -> bool:
        self.hud_turno.icone_combate.is_normal = False
        #chamar selecionar_territorio para escolher o atacante
        #realcar os vizinhos do territorio atacante
        etapa_em_andamento = True
        pulou_turno = False #  Para indicar caso o jogador nao vai fazer nada na etapa 2 e 3 do turno
        while etapa_em_andamento:
            
            self.gerenciador_mapa.selecionar_territorio(self.mouse, jogador)
            if(len(self.gerenciador_mapa.territorios_selecionados)>=1):
                self.hud_combate.atualiza_atacante(self.gerenciador_mapa.territorios_selecionados[0].nome)
            
            self.gerenciador_mapa.selecionar_vizinho(self.mouse, jogador, self.etapa_turno)
            if(len(self.gerenciador_mapa.territorios_selecionados)==2):
                self.hud_combate.atualiza_defensor(self.gerenciador_mapa.territorios_selecionados[1].nome)
            
            codigo_hud_combate = self.hud_combate.update()
            if codigo_hud_combate == 1:
                pass
            elif codigo_hud_combate == 2:
                self.gerenciador_mapa.limpa_territorios_selecionados()
                self.hud_combate.atualiza_atacante("")
                self.hud_combate.atualiza_defensor("")

            # Condicionais para terminar a etapa
            if self.hud_turno.finalizar.update():
                etapa_em_andamento = False
            elif self.hud_turno.pular.update():
                etapa_em_andamento = False
                pulou_turno = True

            self.render()
            self.janela.update()

        self.gerenciador_mapa.territorios_selecionados = []
        self.hud_turno.icone_combate.is_normal = True
        return pulou_turno

    def movimentacao_exercitos(self, jogador) -> None:
        etapa_andamento = True
        while etapa_andamento:
            pass
        self.hud_turno.icone_movimento.is_normal = False
        self.hud_turno.icone_movimento.is_normal = True