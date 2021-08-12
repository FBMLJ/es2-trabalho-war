from PPlay.gameimage import *
from PPlay.window import *
from servico.firestore import db
from firebase_admin import firestore
from componentes.RetanguloTexto import *
from datetime import *
from PPlay.sprite import *
import pygame
from componentes.campoTexto import *
from componentes.campoSenha import *
from componentes.botao import *


class BuscaSaguao:

    def __init__(self, janela: Window, usuario: str):

        self.janela = janela
        self.database = db
        self.usuario = usuario
        self.fundo = GameImage("assets/imagem/busca_saguao/buscador_saguao.png")
        self.fundo.set_position(janela.width/2 - self.fundo.width/2, janela.height/2 - self.fundo.height/2)

        self.busca_pelo_nome = 20
        self.entrar = 21
        self.criar_partida = 22

        self.botoes = []

        buscar_saguao_sprite_normal = Sprite("assets/imagem/busca_saguao/botao_buscar.png")
        buscar_saguao_sprite_destacado = Sprite("assets/imagem/busca_saguao/busca_saguao_select.png")
        botao_busca_saguao = Botao(buscar_saguao_sprite_normal, buscar_saguao_sprite_destacado, self.busca_pelo_nome)
        botao_busca_saguao.setposition(
            self.fundo.x + 30,
            self.fundo.y + self.fundo.height - self.janela.height*0.17
        )
        self.botoes.append(botao_busca_saguao)

        entrar_saguao_sprite_normal = Sprite("assets/imagem/busca_saguao/botao_entrar.png")
        entrar_saguao_sprite_destacado = Sprite("assets/imagem/busca_saguao/botao_entrar_select.png")
        botao_entrar_saguao = Botao(entrar_saguao_sprite_normal, entrar_saguao_sprite_destacado, self.entrar)
        botao_entrar_saguao.setposition(
            self.fundo.x + 30,
            self.fundo.y + self.fundo.height - self.janela.height*0.10
        )
        self.botoes.append(botao_entrar_saguao)

        criar_saguao_sprite_normal = Sprite("assets/imagem/busca_saguao/botao_criar.png")
        criar_saguao_sprite_destacado = Sprite("assets/imagem/busca_saguao/botao_criar_select.png")
        botao_criar_saguao = Botao(criar_saguao_sprite_normal, criar_saguao_sprite_destacado, self.criar_partida)
        botao_criar_saguao.setposition(
            self.fundo.x + self.fundo.width - criar_saguao_sprite_destacado.width - self.janela.width*0.055,
            self.fundo.y + self.fundo.height - self.janela.height*0.10
        )
        self.botoes.append(botao_criar_saguao)

        self.campo_busca_saguao = CampoTexto(
            janela,
            "Digite o nome do saguão",
            self.fundo.x + 30,
            self.fundo.y + self.fundo.height - self.janela.height*0.28,
            self.janela.width * 0.23,
            self.janela.height * 0.06,
            20,
            16
        )

        self.campo_nome_sala = CampoTexto(
            janela,
            "Digite o nome da sala",
            self.fundo.x + self.fundo.width - self.janela.width * 0.15 - self.janela.width*0.04,
            self.fundo.y + self.fundo.height - self.janela.height * 0.28,
            self.janela.width * 0.15,
            self.janela.height * 0.05,
            17,
            14
        )

        self.campo_senha_sala = CampoSenha(
            janela,
            "Digite a senha da sala",
            self.fundo.x + self.fundo.width - self.janela.width * 0.15 - self.janela.width*0.04,
            self.fundo.y + self.fundo.height - self.janela.height * 0.20,
            self.janela.width * 0.15,
            self.janela.height * 0.05,
            17,
            14
        )

        self.saguoes = []
        self.consulta_saguoes = None

    def loop(self):

        self.janela.clear()
        botao_foi_clicado = False
        saguao_foi_clicado = False
        botao_clicado  = -1
        saguao_clicado = -1
        mouse = Mouse()
        self.janela.input_pygame = True

        while True:

            for botao in self.botoes:
                clicou = botao.update()
                if clicou:
                    botao_foi_clicado = True  # bloqueia o botao de ser clicado
                    botao_clicado = botao.code

            for saguao in self.saguoes:
                clicou = saguao.update()
                if clicou:
                    saguao_foi_clicado = True
                    self.saguoes[saguao_clicado].selecionado = False
                    saguao_clicado = saguao.code

            if botao_foi_clicado and not mouse.is_button_pressed(1):
                botao_foi_clicado = False
                if botao_clicado == self.busca_pelo_nome:
                    self.buscaSaguoes(self.campo_busca_saguao.texto)
                if botao_clicado == self.entrar:
                    pass
                if botao_clicado == self.criar_partida:
                    self.criaSaguao()

            if saguao_foi_clicado and not mouse.is_button_pressed(1):
                if saguao_clicado != -1:
                    self.saguoes[saguao_clicado].selecionado = True

            self.trataEvento()
            self.render()
            self.janela.update()

    def render(self):

        self.janela.set_background_color([0, 0, 0])
        self.fundo.draw()
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
                self.fundo.x + 50,
                pos_inicial + tamanho_acumulado + 10 + i * 12
            )

            tamanho_acumulado += 35

    def criaSaguao(self):

        dados = {
            "nome": self.campo_nome_sala.texto,
            "senha": self.campo_senha_sala.texto,
            "data_criacao": datetime.now(),
            "numero_de_jogadores": 1,
            "anfitriao": self.usuario
        }

        db.collection("saguoes").\
            document(self.usuario)\
            .set(dados)
