from telas.Cadastro import Cadastro
import pygame
from PPlay import window
from telas.Cadastro import Cadastro

janela = window.Window(800,400)
l = Cadastro(janela)


while 1:
    
     
    janela.set_background_color((0,0,0))  
    l.draw()
    
    janela.update()

    
