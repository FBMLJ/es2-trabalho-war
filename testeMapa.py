from constant import ALTURA_PADRAO, LARGURA_PADRAO
import pygame
from telas.ControladorMapa import *
from PPlay.window import *
import constant

janela = Window(LARGURA_PADRAO, ALTURA_PADRAO)
controle_mapa = ControladorMapa(janela)
controle_mapa.loop()