import pygame
import constant
from telas.controleDeTelas import ControleDeTelas
pygame.init()
screen = pygame.display.set_mode(constant.TAMANHO_PADRAO)
pygame.display.set_caption(constant.NOME_JOGO)
clock = pygame.time.Clock()


controleDeTelas = ControleDeTelas(pygame)

while True:

    #apaga tudo do frame anterio
    screen.fill((255,255,255))
    controleDeTelas.exebirTelaAtual()

    #desenha tudo no novo frame
    pygame.display.flip()

    #limita fps em 60
    clock.tick(60)
pygame.quit()