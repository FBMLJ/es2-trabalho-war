from componentes.ItemDoHistorico import *
from componentes.PartidaInfo import *
from servico.firestore import db
from PPlay.gameimage import *
from constant import estados
from PPlay.window import *
from firebase_admin import firestore


class HistoricoDePartidas:

    def __init__(self, janela: Window, usuario):

        self.janela = janela
        self.database = db
        self.usuario = usuario

        self.partidas = []

        self.fundo = GameImage("assets/imagem/historico/fundo_historico.png")
        self.barra_superior = GameImage("assets/imagem/historico/barra_superior.png")

        self.botoes = []

        self.partida_info = PartidaInfo(self.janela, 22, [255, 255, 255])
        self.partida_info.set_position(
            self.janela.width - self.partida_info.moldura.width - 50,
            self.barra_superior.y + self.barra_superior.height + 30
        )

        sprite_x = Sprite("assets/imagem/historico/icon_x.png")
        self.x = Botao(sprite_x, sprite_x, 20)
        self.x.setposition(self.janela.width-self.x.width-15, 15)

    def loop(self):

        self.janela.clear()
        self.janela.set_background_color([0, 0, 0])
        carregando = GameImage("assets/imagem/historico/carregando.png")
        carregando.set_position(self.janela.width/2 - carregando.width/2, self.janela.height/2 - carregando.height/2)
        carregando.draw()
        self.janela.update()

        self.carrega_partidas()

        self.janela.clear()
        mouse = Mouse()
        mouse_foi_clicado = False  # variavel que impede que o usuário clique várias vezes
        botao_clicado = -1

        while True:

            clicou = self.x.update()
            if clicou:
                mouse_foi_clicado = True
                botao_clicado = self.x.code

            for botao in self.botoes:
                clicou = botao.update()
                if clicou:
                    mouse_foi_clicado = True #bloqueia o botao de ser clicado
                    self.botoes[botao_clicado].selecionado = False
                    botao_clicado = botao.code

            if mouse_foi_clicado and not mouse.is_button_pressed(1):  # evitar que seja clicados diversas vezes
                mouse_foi_clicado = False
                if botao_clicado == 20:
                    return estados["menu_logado"]
                else:
                    self.partida_info.atualiza_dados(self.partidas[botao_clicado].to_dict())

            if botao_clicado != -1 and botao_clicado != 20:
                self.botoes[botao_clicado].selecionado = True

            self.render()
            self.janela.update()

    def render(self):
        self.fundo.draw()
        self.barra_superior.draw()
        self.partida_info.render()
        self.x.render()
        for botao in self.botoes:
            botao.render()

    def carrega_partidas(self):

        try:
            self.partidas = self.database.collection("usuarios")\
                .document(self.usuario.uid)\
                .collection("HistoricoDePartidas")\
                .order_by("data_inicio", direction=firestore.Query.DESCENDING)\
                .limit(5)\
                .get()
        except:
            self.partidas = []

        pos_inicial = self.barra_superior.y + self.barra_superior.height
        tamanho_acumulado = 0
        for i in range(len(self.partidas)):

            sprite_normal = Sprite("assets/imagem/historico/slot_derrota_2.png")
            sprite_destacado = Sprite("assets/imagem/historico/slot_derrota_select.png")
            if self.partidas[i].to_dict()["vencedor"]:
                sprite_normal = Sprite("assets/imagem/historico/slot_vitoria_2.png")
                sprite_destacado = Sprite("assets/imagem/historico/slot_vitoria_select.png")

            self.botoes.append(ItemDoHistorico(sprite_normal,
                                               sprite_destacado,
                                               i,
                                               self.partidas[i].to_dict()["data_inicio"],
                                               self.partidas[i].to_dict()["data_fim"],
                                               self.partidas[i].to_dict()["quantidade_de_rodadas"],
                                               self.janela
                                               ))
            self.botoes[i].setposition(
                50,
                pos_inicial + tamanho_acumulado + 20 + i*25
            )

            tamanho_acumulado += sprite_normal.height