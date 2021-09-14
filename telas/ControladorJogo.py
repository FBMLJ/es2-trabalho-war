"""
Classe responsavel por gerenciar e instanciar as diversas telas do jogo
"""
from PPlay.window import *
from telas.HistoricoDePartidas import *
from telas.Saguao import *
from telas.BuscaSaguao import *
from telas.Login import *
from telas.Cadastro import *
from telas.MenuLogado import *
from telas.MenuInicial import *
from jogo.ControladorPartida import ControladorPartida
from constant import estados


class ControladorJogo:

    def __init__(self, janela):
        self.janela = janela
        # armazena o usuario retornado ao fazer login ou cadastro
        self.usuario = None
        # armazena o id do saguão ingressado quando o usuário entrar em um saguão
        self.id_saguao = -1
        # armazena qual o estado atual do jogo, começa no menu principal
        self.estado_do_jogo = estados["menu_inicial"]

    def iniciar_jogo(self):

        # controla o fluxo de telas do jogo
        while True:

            if self.estado_do_jogo == estados["menu_inicial"]:
                menu_inicial = MenuInicial(self.janela)
                self.estado_do_jogo = menu_inicial.loop()

            elif self.estado_do_jogo == estados["login"]:
                login = Login(self.janela)
                self.estado_do_jogo, self.usuario = login.loop()
            
            elif self.estado_do_jogo == estados["cadastro"]:
                cadastro = Cadastro(self.janela)
                self.estado_do_jogo, self.usuario = cadastro.loop()

            elif self.estado_do_jogo == estados["menu_logado"]:
                menu_logado = MenuLogado(self.janela)
                self.estado_do_jogo = menu_logado.loop()

            elif self.estado_do_jogo == estados["historico"]:
                historico = HistoricoDePartidas(self.janela, self.usuario)
                self.estado_do_jogo = historico.loop()

            elif self.estado_do_jogo == estados["buscar_sala"]:
                busca_saguao = BuscaSaguao(self.janela, self.usuario)
                self.estado_do_jogo, self.id_saguao = busca_saguao.loop()
                print("passei aqui")

            elif self.estado_do_jogo == estados["em_saguao"]:
                saguao = Saguao(self.janela, self.usuario, self.id_saguao)
                self.estado_do_jogo = saguao.loop()

            elif self.estado_do_jogo == estados["desconectar"]:
                self.usuario = None
                self.estado_do_jogo = estados["menu_inicial"]

            elif self.estado_do_jogo == estados["sair"]:
                exit(0)

            elif self.estado_do_jogo == estados["partida_local"]:
                controlador_partida = ControladorPartida(self.janela)
                self.estado_do_jogo = controlador_partida.loop()

            else:
                exit(0)
