from componentes.campoTexto import *
from componentes.botao import *
from componentes.RetanguloTexto import *
from firebase_admin import firestore
from constant import estados
from servico.firestore import db
from datetime import datetime
from PPlay.gameimage import *
from PPlay.sprite import *


class Saguao:

    def __init__(self, janela, usuario, id_anfitriao):

        self.janela = janela
        self.fundo = GameImage("assets/imagem/saguao/saguao.png")
        self.fundo.set_position(janela.width/2 - self.fundo.width/2, self.janela.height/2 - self.fundo.height/2)
        self.fundo_real = GameImage("assets/imagem/tela_inicial/fundo.png")
        self.id_anfitriao = id_anfitriao
        self.usuario = usuario

        self.codigo_botoes = {
            "sair": 1,
            "pronto": 2,
            "enviar": 3,
            "iniciar": 4
        }

        self.pronto = id_anfitriao == usuario.uid

        self.botoes = []

        self.barra_superior = GameImage("assets/imagem/saguao/barra_saguao.png")
        self.barra_superior.set_position(self.fundo.x + 12, self.fundo.y + 10)

        posicao_x = self.fundo.x + 95
        posicao_y = self.fundo.y + self.fundo.height - 165
        self.tanquezin_verde = GameImage("assets/imagem/saguao/tank.png")
        self.tanquezin_verde.set_position(posicao_x, posicao_y)
        self.tanquezin_vermelho = GameImage("assets/imagem/saguao/tank_ready.png")
        self.tanquezin_vermelho.set_position(posicao_x, posicao_y)

        sprite_x = Sprite("assets/imagem/saguao/x_saguao.png")
        botao_x = Botao(sprite_x, sprite_x, self.codigo_botoes["sair"])
        botao_x.setposition(self.fundo.x + self.fundo.width - botao_x.width - 16, self.fundo.y + 15)
        self.botoes.append(botao_x)

        sprite_enviar_normal = Sprite("assets/imagem/saguao/botao_enviar.png")
        sprite_enviar_destacado = Sprite("assets/imagem/saguao/botao_enviar_select.png")
        botao_enviar = Botao(sprite_enviar_normal, sprite_enviar_destacado, self.codigo_botoes["enviar"])
        botao_enviar.setposition(
            self.fundo.x + self.fundo.width - botao_enviar.width - 40,
            self.fundo.y + self.fundo.height - botao_enviar.height - 40
        )
        self.botoes.append(botao_enviar)
        
        if self.usuario.uid == id_anfitriao:
            caminho_pronto = "assets/imagem/saguao/botao_iniciar.png"
            caminho_pronto_destacado = "assets/imagem/saguao/botao_iniciar_select.png"
            codigo_botao = self.codigo_botoes["iniciar"]
        else:
            caminho_pronto = "assets/imagem/saguao/botao_pronto.png"
            caminho_pronto_destacado = "assets/imagem/saguao/botao_pronto_select.png"
            codigo_botao = self.codigo_botoes["pronto"]
            
        sprite_pronto_normal = Sprite(caminho_pronto)
        sprite_pronto_destacado = Sprite(caminho_pronto_destacado)
        botao_pronto = Botao(sprite_pronto_normal, sprite_pronto_destacado, codigo_botao)
        botao_pronto.setposition(
            self.fundo.x + 80,
            self.fundo.y + self.fundo.height - botao_pronto.height - 40
        )
        self.botoes.append(botao_pronto)

        self.campo_chat = CampoTexto(
            janela,
            GameImage("assets/imagem/saguao/digite_mensagem.png"),
            self.fundo.x + self.fundo.width - 640,
            self.fundo.y + self.fundo.height - botao_pronto.height - 36,
            450,
            50,
            25
        )

        self.legenda_participantes = GameImage("assets/imagem/saguao/participantes.png")
        self.legenda_participantes.set_position(
            self.fundo.x + 50,
            self.barra_superior.y + self.barra_superior.height + 10
        )

        self.legenda_chat = GameImage("assets/imagem/saguao/chat.png")
        self.legenda_chat.set_position(
            self.fundo.x + self.fundo.width - self.legenda_chat.width - 300,
            self.barra_superior.y + self.barra_superior.height + 10
        )

        self.participantes = []
        self.participantes_retangulos = []
        self.mensagens = []
        self.mensagens_retangulos = []

    def loop(self):

        self.carregaParticipantes()
        self.lerMensagens()
        self.janela.clear()
        self.janela.set_background_color([0, 0, 0])
        self.janela.input_pygame = True

        botao_clicado = -1
        clicou_botao = False
        clicou = False
        mouse = Mouse()

        while True:

            for botao in self.botoes:
                clicou = botao.update()
                if clicou:
                    clicou_botao = True
                    botao_clicado = botao.code

            if clicou_botao and not mouse.is_button_pressed(1):
                clicou_botao = False
                if botao_clicado == self.codigo_botoes["sair"]:
                    self.janela.input_pygame = False
                    return estados["buscar_sala"]
                
                if botao_clicado == self.codigo_botoes["pronto"]:
                    self.trocaEstado()
                
                if botao_clicado == self.codigo_botoes["enviar"]:
                    self.enviarMensagem(self.campo_chat.texto)
                    self.campo_chat.texto = ""

            self.trataEvento()
            self.render()
            self.janela.update()

    def trataEvento(self):

        for evento in pygame.event.get():
            self.campo_chat.evento(evento)
            if evento.type == pygame.QUIT:
                exit()

    def render(self):

        self.fundo_real.draw()
        self.fundo.draw()
        self.barra_superior.draw()
        self.campo_chat.draw()
        self.legenda_participantes.draw()
        self.legenda_chat.draw()
        if self.pronto:
            self.tanquezin_verde.draw()
        else:
            self.tanquezin_vermelho.draw()
        for mensagem in self.mensagens_retangulos:
            mensagem.render()
        for participante in self.participantes_retangulos:
            participante.render()
        for botao in self.botoes:
            botao.render()

    def carregaParticipantes(self):

        db.collection('saguoes')\
            .document(self.id_anfitriao)\
            .collection('participantes').on_snapshot(self.escutaParticipantes)

    def escutaParticipantes(self, col_snapshot, changes, read_time):

        self.participantes = []
        self.participantes_retangulos = []

        i = 0
        tamanho_acumulado = 0
        for documento in col_snapshot:

            doc = documento.to_dict()
            self.participantes.append(doc)
            self.participantes_retangulos.append(
                RetanguloTexto(
                    self.janela,
                    doc["nome"],
                    0,
                    200,
                    30
                )
            )
            if doc["pronto"]:
                self.participantes_retangulos[i].cor_atual = (50, 205, 50)
            else:
                self.participantes_retangulos[i].cor_atual = (255, 0, 0)

            self.participantes_retangulos[i].set_position(
                self.fundo.x + 45,
                self.barra_superior.y + self.barra_superior.height + 50 + tamanho_acumulado + i*10
            )
            tamanho_acumulado += 30
            i += 1
    
    def trocaEstado(self):
        
        if self.pronto:
            self.pronto = False
        else:
            self.pronto = True

        novos_dados = {
            "nome": self.usuario.display_name,
            "id_usuario": self.usuario.uid,
            "pronto": self.pronto
        }

        db.collection("saguoes").document(self.id_anfitriao).collection("participantes").document(self.usuario.uid).set(novos_dados)

    # Funcao para enviar mensagem para a subcolecao de chat_saguao do respectivo saguao
    def enviarMensagem(self, msg):
        user_name = self.usuario.display_name
        hora_envio = datetime.now()
        db.collection("saguoes").document(self.id_anfitriao).collection("chat_saguao").add({"msg": msg, "remetente": user_name, "hora_envio": hora_envio})

    # Funcao para ler as mensagens do chat do saguao no banco de dados
    def lerMensagens(self):
        db.collection('saguoes')\
            .document(self.id_anfitriao)\
            .collection('chat_saguao')\
            .order_by("hora_envio", direction=firestore.Query.DESCENDING)\
            .limit(8)\
            .on_snapshot(self.escutaMensagens)

    def escutaMensagens(self, col_snapshot, changes, read_time):
        self.mensagens = []
        self.mensagens_retangulos = []

        i = 0
        tamanho_acumulado = 0
        for documento in col_snapshot:

            doc = documento.to_dict()
            self.mensagens.append(doc)
            self.mensagens_retangulos.append(
                RetanguloTexto(
                    self.janela,
                    doc["remetente"] + ": " + doc["msg"],
                    69,
                    580,
                    30,
                    moldura=False
                )
            )

            self.mensagens_retangulos[i].set_position(
                self.fundo.x + 295,
                self.barra_superior.y + self.barra_superior.height + 50 + tamanho_acumulado + i*10
            )
            tamanho_acumulado += 30
            i += 1