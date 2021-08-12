from PPlay.window import *
from PPlay.gameimage import *
from componentes.Texto import *


class PartidaInfo:

    def __init__(self, janela: Window, tamanho_da_fonte, cor_do_texto):

        self.janela = janela
        self.moldura = GameImage("assets/imagem/historico/detalhes2.png")

        self.tamanho_da_fonte = tamanho_da_fonte
        self.cor_do_texto = cor_do_texto

        self.textos = []

    def render(self):

        self.moldura.draw()

        for texto in self.textos:
            texto.draw()

    def set_position(self, x, y):

        self.moldura.set_position(x, y)

        for i in range(len(self.textos)):
            self.textos[i].set_position(x + 10, y + 45 + i*50)

    def atualiza_dados(self, dados):

        self.textos = []

        self.textos.append(Texto(
            self.janela,
            "Número de Territórios Conquistados: {}".format(dados["numero_de_territorios_conquistados"]),
            self.tamanho_da_fonte,
            self.cor_do_texto
        ))

        self.textos.append(Texto(
            self.janela,
            "Objetivo: {}".format(dados["objetivo"]),
            self.tamanho_da_fonte,
            self.cor_do_texto
        ))

        self.textos.append(Texto(
            self.janela,
            "Número Máximo de Tropas: {}".format(dados["numero_maximo_de_tropas"]),
            self.tamanho_da_fonte,
            self.cor_do_texto
        ))

        self.textos.append(Texto(
            self.janela,
            "Número de Tropas Eliminadas: {}".format(dados["numero_de_tropas_eliminadas"]),
            self.tamanho_da_fonte,
            self.cor_do_texto
        ))

        self.textos.append(Texto(
            self.janela,
            "Quantidade de Trocas: {}".format(dados["quantidade_de_trocas"]),
            self.tamanho_da_fonte,
            self.cor_do_texto
        ))

        self.textos.append(Texto(
            self.janela,
            "Número de Continentes Conquistados: {}".format(dados["numero_de_continentes_conquistados"]),
            self.tamanho_da_fonte,
            self.cor_do_texto
        ))

        self.set_position(self.moldura.x, self.moldura.y)