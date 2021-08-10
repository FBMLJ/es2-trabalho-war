from componentes.botao import *
from PPlay.window import *


class ItemDoHistorico(Botao):

    def __init__(self, sprite_normal, sprite_destacado, codigo, data_inicio, data_fim, qtd_rodadas, janela: Window):

        super().__init__(sprite_normal, sprite_destacado, codigo)

        self.selecionado = False

        duracao_s = data_fim - data_inicio
        duracao_s = duracao_s.total_seconds()
        self.duracao = divmod(duracao_s, 60*60)[0]

        data_inicio = data_inicio.strftime('%d/%m/%Y %H:%M')

        self.tamanho_fonte = 18

        self.posicao_duracao_x = 0
        self.posicao_duracao_y = 0

        self.data_inicio = data_inicio
        self.posicao_data_inicio_x = 0
        self.posicao_data_inicio_y = 0

        self.qtd_rodadas = qtd_rodadas
        self.posicao_qtd_rodadas_x = 0
        self.posicao_qtd_rodadas_y = 0

        self.janela = janela

    def render(self):

        if self.selecionado:
            self.spriteAtual = 1

        super().render()
        self.janela.draw_text("Data de Início: {}".format(self.data_inicio),
                              self.posicao_data_inicio_x,
                              self.posicao_data_inicio_y,
                              self.tamanho_fonte,
                              [0, 0, 0])

        self.janela.draw_text("Duracao: {}h".format(int(self.duracao)),
                              self.posicao_duracao_x,
                              self.posicao_duracao_y,
                              self.tamanho_fonte,
                              [0, 0, 0])

        self.janela.draw_text("Qtd.rodadas: {}".format(self.qtd_rodadas),
                              self.posicao_qtd_rodadas_x,
                              self.posicao_qtd_rodadas_y,
                              self.tamanho_fonte,
                              [0, 0, 0])

    def setposition(self, x, y):
        super().setposition(x, y)

        self.posicao_qtd_rodadas_x = x + 300
        self.posicao_qtd_rodadas_y = y + 20

        self.posicao_data_inicio_x = x + 300
        self.posicao_data_inicio_y = y + 40

        self.posicao_duracao_x = x + 300
        self.posicao_duracao_y = y + 60
