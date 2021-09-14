"""
Classe responsavel pela interface de buscar saguão e sua comunicação com o banco de dados
"""
from servico.firestore import db
from constant import estados
from firebase_admin import firestore
from componentes.RetanguloTexto import *
from datetime import *
from componentes.SenhaSalaPopUp import *
from componentes.MensagemDeErro import *


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

        # define um codigo para identificar cada botao
        self.busca_pelo_nome = 20
        self.criar_partida = 22
        self.sair = 23

        # Inicializa todos os botões da tela em suas devidas posições e os armazena em um vetor para uso posterior
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

        self.saguoes = []  # variável que armazena as representações de saguões que aparecem na tela
        self.consulta_saguoes = None  # Variável que armazena o resultado da consulta mais atual dos saguões
        self.in_popup = False  # variável que indica se o a tela está com um popup ou não. Serve para controlar o fluxo da execução

        # popup que será desenhado caso o usuário clique em uma sala com senha.
        self.popup = SenhaPopUp(janela)
        self.mensagem_popup = MensagemDeErro(janela, "")

    # função que executa o fluxo da tela e controla o comportamento das interações com o usuário
    def loop(self):

        # limpa a janela para evitar resíduos de outras telas
        self.janela.clear()

        # Mostra na tela uma imagem de carregando enquanto um código de inicialização é executado
        self.janela.set_background_color([0, 0, 0])
        carregando = GameImage("assets/imagem/historico/carregando.png")
        carregando.set_position(self.janela.width / 2 - carregando.width / 2,
                                self.janela.height / 2 - carregando.height / 2)
        carregando.draw()
        self.janela.update()

        # inicializa variáveis de controle da interação com o usuário
        botao_foi_clicado = False
        saguao_foi_clicado = False
        botao_clicado  = -1
        saguao_clicado = -1
        mouse = Mouse()
        self.janela.input_pygame = True  # necessário quando a tela possuir campos de preenchimento
        self.buscaSaguoes("")  # executa uma busca inicial para obter os saguões disponíveis

        while True:

            # para cada botão armazenado veririca se o mesmo foi clicado
            for botao in self.botoes:
                clicou = botao.update()
                if clicou:
                    botao_foi_clicado = True  # bloqueia o botao de ser clicado
                    botao_clicado = botao.code

            # para cada saguão gerado pela busca, verifica se o mesmo foi clicado
            for saguao in self.saguoes:
                clicou = saguao.update()
                if clicou:
                    saguao_foi_clicado = True
                    # esse if controla o duplo clique.
                    # se um saguão for clicado apenas uma vez, reseta o clique.
                    if not saguao_clicado == saguao.code:
                        self.saguoes[saguao_clicado].selecionado = False
                    # armazena qual saguão foi clicado
                    saguao_clicado = saguao.code

            # esse garante que um clique só será efetivado uma vez que o botão do mouse seja solto
            if botao_foi_clicado and not mouse.is_button_pressed(1):

                # se algum botão foi clicado, reseta a variável de controle do clique
                botao_foi_clicado = False

                if botao_clicado == self.busca_pelo_nome:
                    # busca saguões no banco de dados de acordo com o nome informado pelo usuário
                    self.buscaSaguoes(self.campo_busca_saguao.texto)

                if botao_clicado == self.sair:
                    # desativa a opção de input pelo pygame
                    self.janela.input_pygame = False
                    # retorna ao menu logado
                    return estados["menu_logado"], -1

                if botao_clicado == self.criar_partida:
                    # cria a partida com as especificações desejadas
                    campos_sao_validos, mensagem_de_erro = self.confere_campos_da_criacao(self.campo_nome_sala.texto,
                                                                                          self.campo_senha_sala.texto)
                    if campos_sao_validos:
                        self.criaSaguao(self.campo_senha_sala.texto, self.campo_nome_sala.texto)
                        return estados["em_saguao"], self.usuario.uid
                    else:
                        self.mensagem_popup.mensagem = mensagem_de_erro
                        self.mostra_mensagem_de_erro(mouse)

            if saguao_foi_clicado and not mouse.is_button_pressed(1):

                saguao_foi_clicado = False
                # verifica se o saguão clicado é válido
                if saguao_clicado != -1:
                    # se o saguão clicado já foi selecionado, então ocorreu um clique duplo
                    if self.saguoes[saguao_clicado].selecionado:
                        if self.consulta_saguoes[saguao_clicado].to_dict()["senha"] != "":
                            # muda para o modo de popup, para pedir ao usuário a senha da saka
                            self.in_popup = True
                            sucesso = self.mostra_popup_de_senha(saguao_clicado, mouse)
                            if sucesso:
                                return estados["em_saguao"], self.consulta_saguoes[saguao_clicado].to_dict()[
                                    "anfitriao"]
                        else:
                            sucesso = self.entrar_no_saguao(saguao_clicado)
                            if sucesso:
                                return estados["em_saguao"], self.consulta_saguoes[saguao_clicado].to_dict()["anfitriao"]
                        saguao_clicado = -1
                    else:
                        # se é a primeira vez que o saguão é selecionado
                        # altera a variável que dá o feedback de seleção
                        self.saguoes[saguao_clicado].selecionado = True

            self.trataEvento()
            self.render()
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

    # função que busca saguões no banco de dados
    def buscaSaguoes(self, nome):

        # limpa os valores desatualizados dos saguões
        self.saguoes = []

        # se não foi especificado um nome para o saguão a se buscar
        if nome == "":

            # busca os 6 saguões mais recentes
            self.consulta_saguoes = self.database.collection("saguoes")\
                .order_by("data_criacao", direction=firestore.Query.DESCENDING)\
                .limit(6)\
                .get()

        # se foi especificado um nome
        else:
            # busca o saguão com o nome fornecido
            self.consulta_saguoes = self.database.collection("saguoes")\
                .where('nome', '==', nome)\
                .limit(6)\
                .get()

        # gera as representações dos saguẽs buscados na tela
        # uma embaixo da outra, a partir de uma posição inicial
        pos_inicial = self.fundo.y + 30
        tamanho_acumulado = 0

        # para cada saguão buscado, cria o objeto referente ao mesmo
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
            # seta a posição do objeto mais recente em relação aos anteriores
            self.saguoes[i].set_position(
                self.fundo.x + 65,
                pos_inicial + tamanho_acumulado + 45 + i * 12
            )

            tamanho_acumulado += 35

    # Função que cria um saguão no banco de dados
    def criaSaguao(self, senha: str, nome: str):

        # cria o dicionário dos dados que serão guardados no banco
        dados = {
            "nome": nome,
            "senha": senha,
            "data_criacao": datetime.now(),
            "numero_de_jogadores": 1,
            "anfitriao": self.usuario.uid,
        }

        # guarda o dicionário gerado no banco
        db.collection("saguoes").\
            document(self.usuario.uid)\
            .set(dados)

        # Insere o próprio criador na lista de participantes
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

    # Caso o usuário deseje entrar em um saguão já existente, insere o usuário na lista de participantes do saguão.
    def entrar_no_saguao(self, saguao_clicado):

        mouse = Mouse()

        sala_atualizada = db.collection("saguoes") \
            .document(self.consulta_saguoes[saguao_clicado].to_dict()["anfitriao"]).get()

        if sala_atualizada.to_dict()["numero_de_jogadores"] < 6:

            novo_numero_de_jogadores = sala_atualizada.to_dict()["numero_de_jogadores"] + 1

            db.collection("saguoes") \
                .document(self.consulta_saguoes[saguao_clicado].to_dict()["anfitriao"])\
                .update({"numero_de_jogadores": novo_numero_de_jogadores})

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
            return True
        else:
            self.mensagem_popup.mensagem = "Sala Lotada"
            self.mostra_mensagem_de_erro(mouse)
            return False

    # função que verifica se os campos de criação da sala estão corretos,
    # Caso haja algum problema nos campos retorna falso e uma mensagem de erro
    def confere_campos_da_criacao(self, nome: str, senha: str):

        if nome == "":
            return False, "insira um nome para a sala"
        elif len(nome) >= 10:
            return False, "nome muito grande (> 10)"
        elif len(senha) >= 8:
            return False, "senha muito grande (> 8)"
        return True, ""

    # função que mostra o popup da senha caso seja necessário para entrar na sala
    def mostra_popup_de_senha(self, saguao_clicado, mouse):

        botao_foi_clicado = False
        botao_clicado = -1

        while True:

            # atualiza o popup e verifica se algum botão do popup foi clicado
            retorno_popup = self.popup.update()
            if retorno_popup != 0:
                botao_clicado = retorno_popup
                botao_foi_clicado = True

            if botao_foi_clicado and not mouse.is_button_pressed(1):
                botao_foi_clicado = False
                if botao_clicado == 2:  # se o botão de fechar o popup foi clicado, fecha e reseta o popup
                    self.popup.input.texto = ""
                    return False
                elif botao_clicado == 1:  # se o botão de entrar do popup foi clicado
                    # verifica se a senha inserida na caixa é a correta
                    if self.popup.input.texto == self.consulta_saguoes[saguao_clicado].to_dict()["senha"]:
                        # se a senha for correta envia o usuário a sala desejada
                        return self.entrar_no_saguao(saguao_clicado)
                    else:
                        self.mensagem_popup.mensagem = "Senha incorreta"
                        self.mostra_mensagem_de_erro(mouse)

            self.render()
            self.popup.render()
            self.janela.update()

    # função que entra em um loop de mensagem de erro
    def mostra_mensagem_de_erro(self, mouse):

        botao_foi_clicado = False
        self.janela.input_pygame = False

        while True:

            retorno_mensagem_popup = self.mensagem_popup.update()
            if retorno_mensagem_popup != 0:
                botao_foi_clicado = True

            if botao_foi_clicado and not mouse.is_button_pressed(1):
                self.janela.input_pygame = True
                return

            self.render()
            self.mensagem_popup.render()
            self.janela.update()