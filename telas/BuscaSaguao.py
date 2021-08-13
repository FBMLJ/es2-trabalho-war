from PPlay.gameimage import *
from PPlay.window import *
from servico.firestore import db
from constant import estados
from firebase_admin import firestore
from componentes.RetanguloTexto import *
from datetime import *
from PPlay.sprite import *
import pygame
from componentes.campoTexto import *
from componentes.campoSenha import *
from componentes.botao import *
from componentes.SenhaSalaPopUp import *


class BuscaSaguao:

    def __init__(self, janela: Window, usuario):

        self.janela = janela
        self.database = db
        self.usuario = usuario
        self.fundo = GameImage("assets/imagem/busca_saguao/buscador_saguao.png")
        self.fundo.set_position(janela.width/2 - self.fundo.width/2, janela.height/2 - self.fundo.height/2)
        self.fundo_real = GameImage("assets/imagem/tela_inicial/fundo.png")

        self.barra_superior = GameImage("assets/imagem/busca_saguao/barra_superior_busca.png")
        self.barra_superior.set_position(self.fundo.x+12, self.fundo.y+10)

        self.busca_pelo_nome = 20
        self.entrar = 21
        self.criar_partida = 22
        self.sair = 23

        self.botoes = []

        sprite_x = Sprite("assets/imagem/busca_saguao/x_saguao.png")
        botao_x = Botao(sprite_x, sprite_x, self.sair)
        botao_x.setposition(self.fundo.x + self.fundo.width - botao_x.width - 17, self.fundo.y + 15)
        self.botoes.append(botao_x)

        buscar_saguao_sprite_normal = Sprite("assets/imagem/busca_saguao/botao_buscar.png")
        buscar_saguao_sprite_destacado = Sprite("assets/imagem/busca_saguao/busca_saguao_select.png")
        botao_busca_saguao = Botao(buscar_saguao_sprite_normal, buscar_saguao_sprite_destacado, self.busca_pelo_nome)
        botao_busca_saguao.setposition(
            self.fundo.x + 50,
            self.fundo.y + self.fundo.height - self.janela.height*0.23
        )
        self.botoes.append(botao_busca_saguao)

        criar_saguao_sprite_normal = Sprite("assets/imagem/busca_saguao/botao_criar.png")
        criar_saguao_sprite_destacado = Sprite("assets/imagem/busca_saguao/botao_criar_select.png")
        botao_criar_saguao = Botao(criar_saguao_sprite_normal, criar_saguao_sprite_destacado, self.criar_partida)
        botao_criar_saguao.setposition(
            self.fundo.x + self.fundo.width - criar_saguao_sprite_destacado.width - self.janela.width*0.1,
            self.fundo.y + self.fundo.height - self.janela.height*0.10
        )
        self.botoes.append(botao_criar_saguao)

        titulo = GameImage("assets/imagem/busca_saguao/busca_pelo_nome.png")
        self.campo_busca_saguao = CampoTexto(
            janela,
            titulo,
            self.fundo.x + 50,
            self.fundo.y + self.fundo.height - self.janela.height*0.30,
            self.janela.width * 0.27,
            self.janela.height * 0.05,
            20
        )

        titulo = GameImage("assets/imagem/busca_saguao/nome_da_sala.png")
        self.campo_nome_sala = CampoTexto(
            janela,
            titulo,
            self.fundo.x + self.fundo.width - self.janela.width * 0.15 - self.janela.width*0.112,
            self.fundo.y + self.fundo.height - self.janela.height * 0.30,
            self.janela.width * 0.20,
            self.janela.height * 0.05,
            17
        )

        titulo = GameImage("assets/imagem/busca_saguao/senha_da_sala.png")
        self.campo_senha_sala = CampoSenha(
            janela,
            titulo,
            self.fundo.x + self.fundo.width - self.janela.width * 0.15 - self.janela.width*0.112,
            self.fundo.y + self.fundo.height - self.janela.height * 0.20,
            self.janela.width * 0.20,
            self.janela.height * 0.05,
            17
        )

        self.saguoes = []
        self.consulta_saguoes = None
        self.in_popup = False

        self.popup = SenhaPopUp(janela)

    def loop(self):

        self.janela.clear()
        self.janela.set_background_color([0, 0, 0])
        carregando = GameImage("assets/imagem/historico/carregando.png")
        carregando.set_position(self.janela.width / 2 - carregando.width / 2,
                                self.janela.height / 2 - carregando.height / 2)
        carregando.draw()
        self.janela.update()
        botao_foi_clicado = False
        saguao_foi_clicado = False
        popup_foi_clicado = False
        botao_clicado  = -1
        saguao_clicado = -1
        popup_clicado = -1
        mouse = Mouse()
        self.janela.input_pygame = True
        self.buscaSaguoes("")

        while True:
            
            if not self.in_popup:
                for botao in self.botoes:
                    clicou = botao.update()
                    if clicou:
                        botao_foi_clicado = True  # bloqueia o botao de ser clicado
                        botao_clicado = botao.code

                for saguao in self.saguoes:
                    clicou = saguao.update()
                    if clicou:
                        saguao_foi_clicado = True
                        if not saguao_clicado == saguao.code:
                            self.saguoes[saguao_clicado].selecionado = False
                        saguao_clicado = saguao.code

                if botao_foi_clicado and not mouse.is_button_pressed(1):
                    botao_foi_clicado = False
                    if botao_clicado == self.busca_pelo_nome:
                        self.buscaSaguoes(self.campo_busca_saguao.texto)
                    if botao_clicado == self.entrar:
                        pass
                    if botao_clicado == self.sair:
                        self.janela.input_pygame = False
                        return estados["menu_logado"], -1
                    if botao_clicado == self.criar_partida:
                        self.criaSaguao()
                        return estados["em_saguao"], self.usuario.uid

                if saguao_foi_clicado and not mouse.is_button_pressed(1):
                    saguao_foi_clicado = False
                    if saguao_clicado != -1:
                        if self.saguoes[saguao_clicado].selecionado:
                            self.in_popup = True
                            self.saguao_clicado = -1
                        else:
                            self.saguoes[saguao_clicado].selecionado = True
                self.trataEvento()
                self.render()

            else:
                retorno_popup = self.popup.update()
                if retorno_popup != 0:
                    popup_clicado = retorno_popup
                    popup_foi_clicado = True

                if popup_foi_clicado and not mouse.is_button_pressed(1):
                    popup_foi_clicado = False
                    if popup_clicado == 2:
                        self.in_popup = False
                        self.popup.input.texto = ""
                        continue
                    elif popup_clicado == 1:
                        if self.popup.input.texto == self.consulta_saguoes[saguao_clicado].to_dict()["senha"] or self.consulta_saguoes[saguao_clicado].to_dict()["senha"] == "":
                            self.entrar_no_saguao(saguao_clicado)
                            return estados["em_saguao"], self.consulta_saguoes[saguao_clicado].to_dict()["anfitriao"]
                        else:
                            print(":(")
                self.render()
                self.popup.render()
            self.janela.update()

    def render(self):

        self.fundo_real.draw()
        self.fundo.draw()
        self.barra_superior.draw()
        self.campo_busca_saguao.draw()
        self.campo_nome_sala.draw()
        self.campo_senha_sala.draw()
        for saguao in self.saguoes:
            saguao.render()
        for botao in self.botoes:
            botao.render()

    def trataEvento(self):

        for evento in pygame.event.get():
            self.campo_busca_saguao.evento(evento)
            self.campo_nome_sala.evento(evento)
            self.campo_senha_sala.evento(evento)
            if evento.type == pygame.QUIT:
                exit()

    def buscaSaguoes(self, nome):

        self.saguoes = []

        if nome == "":

            self.consulta_saguoes = self.database.collection("saguoes")\
                .order_by("data_criacao", direction=firestore.Query.DESCENDING)\
                .limit(6)\
                .get()

        else:

            self.consulta_saguoes = self.database.collection("saguoes")\
                .where('nome', '==', nome)\
                .limit(6)\
                .get()

        pos_inicial = self.fundo.y + 30
        tamanho_acumulado = 0
        for i in range(len(self.consulta_saguoes)):

            self.saguoes.append(
                RetanguloTexto(
                    self.janela,
                    self.consulta_saguoes[i].to_dict()["nome"],
                    i,
                    self.fundo.width - 150,
                    35,
                    22
                )
            )
            self.saguoes[i].set_position(
                self.fundo.x + 65,
                pos_inicial + tamanho_acumulado + 45 + i * 12
            )

            tamanho_acumulado += 35

    def criaSaguao(self):

        dados = {
            "nome": self.campo_nome_sala.texto,
            "senha": self.campo_senha_sala.texto,
            "data_criacao": datetime.now(),
            "numero_de_jogadores": 1,
            "anfitriao": self.usuario.uid
        }

        db.collection("saguoes").\
            document(self.usuario.uid)\
            .set(dados)

        dados_participante = {
            "nome": self.usuario.display_name,
            "id_usuario": self.usuario.uid,
            "pronto": True
        }

        db.collection("saguoes") \
            .document(self.usuario.uid) \
            .collection("participantes")\
            .document(self.usuario.uid)\
            .set(dados_participante)

    def entrar_no_saguao(self, saguao_clicado):
        dados_participante = {
            "nome": self.usuario.display_name,
            "id_usuario": self.usuario.uid,
            "pronto": False
        }

        db.collection("saguoes") \
            .document(self.consulta_saguoes[saguao_clicado].to_dict()["anfitriao"]) \
            .collection("participantes")\
            .document(self.usuario.uid)\
            .set(dados_participante)