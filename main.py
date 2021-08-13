from PPlay import window
import pygame
from telas.HistoricoDePartidas import *
from telas.MenuInicial import *
from telas.ControladorJogo import *
from servico.firestore import db
from telas.Login import *
from datetime import *
from time import sleep
from telas.Saguao import *
from telas.BuscaSaguao import *
import constant

janela = window.Window(constant.LARGURA_PADRAO, constant.ALTURA_PADRAO)
janela.set_title("War Online")

jogo = ControladorJogo(janela)
jogo.iniciar_jogo()

# inserção de dados de teste do historico de partidas para um novo usuario
"""
login = Login(janela)

sucesso, resultado = login.loop()

if sucesso:
    partidas = db.collection("usuarios") \
        .document("wd2xmut0prTgv8FcT1Z4O6UDJxP2") \
        .collection("HistoricoDePartidas") \
        .order_by("data_inicio", direction=firestore.Query.DESCENDING) \
        .limit(10) \
        .get()

    for partida in partidas:
        db.collection("usuarios").document(resultado.uid).collection("HistoricoDePartidas").add(partida.to_dict())
"""

#Inserção de dados de teste nos bancos
"""""
data_inicio = datetime.strptime("06/03/2021 11:00", "%d/%m/%Y %H:%M")
data_fim = datetime.strptime("06/03/2021 21:15", "%d/%m/%Y %H:%M")

dados_historico = {
    "quantidade_de_rodadas": 300,
    "data_inicio": data_inicio,
    "data_fim": data_fim,
    "vencedor": True,
    "numero_de_territorios_conquistados": 26,
    "objetivo": "testar o bd 6",
    "numero_maximo_de_tropas": 60,
    "numero_de_tropas_eliminadas": 110,
    "quantidade_de_trocas": 2,
    "numero_de_continentes_conquistados": 2
}

dados_usuario = {
    "id_usuario": "id2",
    "nome_do_usuario": "douglas",
    "numero_de_vitorias": 7,
    "numero_de_derrotas": 8
}

#db.collection("usuarios").document(dados_usuario["id_usuario"]).set(dados_usuario)
db.collection("usuarios").document(dados_usuario["id_usuario"]).collection("HistoricoDePartidas").add(dados_historico)
"""""
