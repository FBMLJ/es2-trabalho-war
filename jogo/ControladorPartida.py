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
from jogo.CombateManager import CombateManager
from componentes.hudTurno import hudTurno
from componentes.hudSelecionaTropas import HudSelecionaTropas
from componentes.hudCombate import HudCombate
from componentes.hudMovimenta import HudMovimenta
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
        self.gerenciador_combate = CombateManager()
        self.jogadores = jogadores
        self.todos_os_objetivos = self.gerenciador_objetivos.gera_objetivos(self.gerenciador_mapa.lista_continentes)        

        self.iniciador_de_partida.distribui_cores(self.jogadores)
        self.iniciador_de_partida.distribui_territorios(self.gerenciador_mapa.lista_territorios, self.jogadores)
        self.iniciador_de_partida.distribui_objetivos(self.todos_os_objetivos, self.jogadores)
            
        self.hud_turno = hudTurno(janela)
        self.hud_seleciona_quantidade = HudSelecionaTropas(janela)
        self.hud_combate = HudCombate(janela)
        self.hud_movimenta = HudMovimenta(janela)
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
                self.distribuicao_exercitos(jogador)
                    
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
                        print("entrei na etapa de movimentacao")
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
        if(self.etapa_turno == 3):
            self.hud_movimenta.render()

    def inicia_cartas(self) -> None:
        for id_territorio in dicionario_territorios:
            nome_territorio = dicionario_territorios[id_territorio]
            imagem = nome_territorio + "_carta.png"
            figura = dicionario_figura_territorio[id_territorio]
            self.todas_as_cartas.append(Card(nome_territorio, imagem, figura, False))

    def distribuicao_exercitos(self, jogador:Player) -> None:
        self.hud_turno.escreve_indicador_turno(jogador.cor, "distribuicao de exercitos")

        self.gerenciador_tropas.recebimento_rodada(jogador, self.gerenciador_mapa.lista_continentes)
        if jogador.bot:
            jogador.distribuir_tropas()
            self.render()
            self.janela.update()
            return
        
        self.hud_turno.icone_distribuir.is_normal = False #  Destacando o icone da etapa de distribuicao de tropas
        self.hud_seleciona_quantidade.maximo = jogador.tropas_pendentes #  Quantidade de tropas a ser distribuida
        self.gerenciador_mapa.territorios_selecionados = []
        
        etapa_concluida = False
        while not etapa_concluida:
            self.gerenciador_mapa.selecionar_territorio(self.mouse, jogador, self.etapa_turno)
            clicou_ok = self.hud_seleciona_quantidade.update(self.mouse)
            if clicou_ok: #  Apos clicar no OK da hud, termina de distribuir tropas para o territorio selecionado
                tropas_distribuidas = self.hud_seleciona_quantidade.quantidade
                self.gerenciador_mapa.territorios_selecionados[0].quantidade_tropas += tropas_distribuidas
                jogador.tropas_pendentes -= tropas_distribuidas
                self.hud_seleciona_quantidade.maximo = jogador.tropas_pendentes
                self.hud_seleciona_quantidade.quantidade = 0
                self.hud_seleciona_quantidade.caixa_quantidade.texto = "0"
                self.gerenciador_mapa.pode_desenhar = True 
                self.gerenciador_mapa.limpa_territorios_selecionados()

            if jogador.tropas_pendentes == 0: #  A etapa termina automaticamente assim que o jogador distribui todas as tropas
                etapa_concluida = True
            
            self.render()
            self.janela.update()
        
        self.gerenciador_mapa.limpa_territorios_selecionados() #  Limpa os territorios selecionados antes de ir para a proxima etapa
        self.hud_turno.icone_distribuir.is_normal = True #  Fazendo o icone da etapa de distribuicao voltar ao normal

    def combate(self, jogador) -> bool:
        self.hud_turno.escreve_indicador_turno(jogador.cor, "combate")
        self.hud_turno.icone_combate.is_normal = False
        etapa_em_andamento = True
        pulou_turno = False #  Para indicar caso o jogador nao vai fazer nada na etapa 2 e 3 do turno
        self.hud_combate.set_etapa_combate(0)

        if jogador.bot:
            
            jogador.escolhe_atacar()
            self.gerenciador_combate.ataques_do_bot(jogador, self.jogadores)
            self.render()
            self.janela.update()
            return pulou_turno

        while etapa_em_andamento:

            #  Primeira parte da etapa de combate: selecao do territorio atacante e defensor
            if self.hud_combate.etapa_combate == 0:
                #  Escolhendo o territorio atacante
                self.gerenciador_mapa.selecionar_inicial(self.mouse, jogador, self.etapa_turno)
                if(len(self.gerenciador_mapa.territorios_selecionados)>=1):
                    self.hud_combate.atualiza_atacante(self.gerenciador_mapa.territorios_selecionados[0].nome)
                #  Escolhando o territorio defensor
                self.gerenciador_mapa.selecionar_vizinho(self.mouse, jogador, self.etapa_turno)
                if(len(self.gerenciador_mapa.territorios_selecionados)==2):
                    self.hud_combate.atualiza_defensor(self.gerenciador_mapa.territorios_selecionados[1].nome)
            
                codigo_hud_combate = self.hud_combate.update(self.mouse)
                #  Passo para a proxima parte do combate
                if codigo_hud_combate == 1: #  Codigo do botao OK da hud de combate
                    self.hud_combate.set_etapa_combate(codigo_hud_combate)
                    tropa_maxima = self.gerenciador_mapa.territorios_selecionados[0].quantidade_tropas -1
                    self.hud_combate.quantidade_maxima = tropa_maxima
                    self.hud_combate.quantidade_atual = tropa_maxima
                    self.hud_combate.caixa_quantidade_atacantes.texto = str(tropa_maxima)
                #  Cancelo as selecoes feitas
                elif codigo_hud_combate == 2: #  Codigo do botao X da hud de combate
                    self.gerenciador_mapa.limpa_territorios_selecionados()
                    self.gerenciador_mapa.pode_desenhar = True
                    self.hud_combate.atualiza_atacante("")
                    self.hud_combate.atualiza_defensor("")
                    codigo_hud_combate = 0

            #Segunda parte da etapa de combate: selecao da quantidade de tropas atacantes
            if self.hud_combate.etapa_combate == 1:

                codigo_hud_combate = self.hud_combate.update(self.mouse)
                if codigo_hud_combate == 3 and len(self.gerenciador_mapa.territorios_selecionados) == 2: #  Botao OK da segunda parte da hud foi clicada
                    for j in self.jogadores:
                        #  Procurando o jogador defensor com base no territorio defensor selecionado
                        if j.possui_territorio(self.gerenciador_mapa.territorios_selecionados[1]):
                            territorio_atacante = self.gerenciador_mapa.territorios_selecionados[0]
                            territorio_defensor = self.gerenciador_mapa.territorios_selecionados[1]
                            tropas_atacantes = self.hud_combate.quantidade_atual
                            
                            conquistou_territorio = self.gerenciador_combate.atacar(
                                                                jogador.territorios, 
                                                                j.territorios,
                                                                territorio_atacante,
                                                                territorio_defensor,
                                                                tropas_atacantes
                                                            )
                            if conquistou_territorio:
                                territorio_defensor.set_cor_tropas(jogador.cor)
                                conquistou_territorio = False

                            self.gerenciador_mapa.pode_desenhar = True
                            self.gerenciador_mapa.limpa_territorios_selecionados()
                            self.hud_combate.set_etapa_combate(0)
                            break

            # Condicionais para terminar a etapa de combate
            if self.hud_turno.finalizar.update():
                etapa_em_andamento = False
            elif self.hud_turno.pular.update():
                etapa_em_andamento = False
                pulou_turno = True

            self.render()
            self.janela.update()

        self.gerenciador_mapa.limpa_territorios_selecionados()
        self.hud_turno.icone_combate.is_normal = True
        self.hud_combate.limpa_hud()
        return pulou_turno

    def movimentacao_exercitos(self, jogador) -> None:
        self.hud_turno.escreve_indicador_turno(jogador.cor, "movimento de tropas")
        self.hud_turno.icone_movimento.is_normal = False
        etapa_em_andamento = True
        
        self.hud_movimenta.set_etapa_movimenta(0)
        
        if jogador.bot:
            jogador.deslocar_tropas()
            self.render()
            self.janela.update()
            return

        while etapa_em_andamento:
            
            #  Primeira parte da etapa de combate: selecao do territorio atacante e defensor
            if self.hud_movimenta.etapa_movimenta == 0:
                #  Escolhendo o territorio inicial que tera sua tropa movida
                self.gerenciador_mapa.selecionar_inicial(self.mouse, jogador, self.etapa_turno)
                if(len(self.gerenciador_mapa.territorios_selecionados)>=1):
                    self.hud_movimenta.atualiza_inicial(self.gerenciador_mapa.territorios_selecionados[0].nome)
                #  Escolhando o territorio de destino que recebera as tropas movidas
                self.gerenciador_mapa.selecionar_vizinho(self.mouse, jogador, self.etapa_turno)
                if(len(self.gerenciador_mapa.territorios_selecionados)==2):
                    self.hud_movimenta.atualiza_destino(self.gerenciador_mapa.territorios_selecionados[1].nome)
            
                codigo_hud_movimenta = self.hud_movimenta.update(self.mouse)
                if codigo_hud_movimenta == 1: #  Passo para a proxima parte do combate
                    self.hud_movimenta.set_etapa_movimenta(codigo_hud_movimenta)
                    tropa_maxima = self.gerenciador_mapa.territorios_selecionados[0].quantidade_tropas -1
                    self.hud_movimenta.quantidade_maxima = tropa_maxima
                    self.hud_movimenta.quantidade_atual = tropa_maxima
                    self.hud_movimenta.caixa_quantidade.texto = str(tropa_maxima)
                elif codigo_hud_movimenta == 2: #  Cancelo as selecoes feitas
                    self.gerenciador_mapa.limpa_territorios_selecionados()
                    self.gerenciador_mapa.pode_desenhar = True
                    self.hud_movimenta.atualiza_inicial("")
                    self.hud_movimenta.atualiza_destino("")
                    codigo_hud_movimenta = 0

            #Segunda parte da etapa de movimentacao: selecao da quantidade de tropas movidas
            if self.hud_movimenta.etapa_movimenta == 1:

                codigo_hud_movimenta = self.hud_movimenta.update(self.mouse)
                movimento_sucesso = False
                if codigo_hud_movimenta == 3 and len(self.gerenciador_mapa.territorios_selecionados) == 2: #  Botao OK da segunda parte da hud foi clicada
                    #print("movimentacao inciada")
                    territorio_inicial = self.gerenciador_mapa.territorios_selecionados[0]
                    territorio_destino = self.gerenciador_mapa.territorios_selecionados[1]
                    tropas_movidas = self.hud_movimenta.quantidade_atual
                    movimento_sucesso = self.gerenciador_tropas.movimenta_tropas(
                                                                                    jogador.territorios,
                                                                                    territorio_inicial,
                                                                                    territorio_destino,
                                                                                    tropas_movidas
                                                                                )
                    self.gerenciador_mapa.pode_desenhar = True
                    self.gerenciador_mapa.limpa_territorios_selecionados()    
                    self.hud_movimenta.set_etapa_movimenta(0)
                    codigo_hud_movimenta = 0


            # Condicionais para terminar a etapa de movimentacao
            if self.hud_turno.finalizar.update() or self.hud_turno.pular.update():
                etapa_em_andamento = False

            self.render()
            self.janela.update()

        self.gerenciador_mapa.limpa_territorios_selecionados()
        self.hud_turno.icone_movimento.is_normal = True
        self.hud_movimenta.limpa_hud()