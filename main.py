import pygame
import constant
from telas.controleDeTelas import ControleDeTelas
pygame.init()
screen = pygame.display.set_mode(constant.TAMANHO_PADRAO)
pygame.display.set_caption(constant.NOME_JOGO)
clock = pygame.time.Clock()


controleDeTelas = ControleDeTelas(pygame, screen,clock)
controleDeTelas.gameLoop()

