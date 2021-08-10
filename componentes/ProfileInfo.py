from typing import Dict
from PPlay.window import *
from PPlay.gameimage import *
from componentes.Texto import *

'''
Classe responsavel por guardar os valores pertinentes ao perfil do jogador,
tambem eh responsavel por buscar tais valores em um banco de dados,
disponibilizar tais valores para exibicao em tela
'''
class ProfileInfo:
    '''
    Construtor da classe, depende de ter um usuario de id para existir.
    '''
    def __init__(self, user_id: int):
        #Atributos pertinentes as infos do perfil
        self.user_id = user_id
        self.partidas_ganhas = 0
        self.partidas_perdidas = 0
        self.nome = "Nome do Jogador"
        #Atributos pertinentes a exibicao das infos
        self.janela = None
        self.moldura = None
        self.tamanho_da_fonte = 0
        self.cor_do_texto = None
        #Vetor de textos para exibicao na tela
        self.textos = []

    '''
    Atribui os campos pertinentes a exibicao do perfil na tela do jogo
    '''
    def setExibicao(self, janela: Window, moldura: GameImage, tamanho_da_fonte: int, cor_do_texto: int[3]) -> None:
        self.janela = janela
        self.moldura = moldura
        self.tamanho_da_fonte = tamanho_da_fonte
        self.cor_do_texto = cor_do_texto

    '''
    Busca pela quantidade de partidas ganhas no Firebase,
    pela quantidade de partidas perdidas no Firebase,
    pelo nome do usuario do Perfil no Firebase
    '''
    def setProfileInfo(self) -> None:
        user = self.db.collection("usuarios")\
            .document(self.user_id).get()

        self.partidas_ganhas = user.to_dict()["numero_de_vitorias"]
        self.partidas_perdidas = user.to_dict()["numero_de_derrotas"]
        self.nome = user.to_dict()["nome_do_usuario"]

    '''
    Metodo para renderizar os campos do Perfil na tela
    '''
    def render(self) -> None:
        self.moldura.draw()
        for texto in self.textos:
            texto.draw()

    '''
    Metodo para atribuir a posicao do quadro que exibira o perfil na tela
    '''
    def set_position(self, x: int, y: int) -> None:
        self.moldura.set_position(x, y)
        margin_left = 10
        margin_top = 150
        padding_top = 50
        for i in range(len(self.textos)):
            self.textos[i].set_position(x + margin_left, y + margin_top + i*padding_top)

    '''
    Atualiza os valores do vetor de textos para exibicao na tela
    '''
    def atualiza_dados(self, dados: Dict) -> None:
        self.textos = []

        self.textos.append(Texto(
            self.janela,
            "Jogador: {}".format(dados["nome"]),
            self.tamanho_da_fonte,
            self.cor_do_texto
        ))

        self.textos.append(Texto(
            self.janela,
            "Partidas Ganhas: {}".format(dados["partidas_ganhas"]),
            self.tamanho_da_fonte,
            self.cor_do_texto
        ))

        self.textos.append(Texto(
            self.janela,
            "Partidas Perdidas: {}".format(dados["partidas_perdidas"]),
            self.tamanho_da_fonte,
            self.cor_do_texto
        ))

        self.set_position(self.moldura.x, self.moldura.y)