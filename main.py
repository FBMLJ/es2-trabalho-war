from telas.Cadastro import Cadastro
import pygame
from PPlay import window
from telas.Login import Login

janela = window.Window(1280,720)
l = Login(janela)


while 1:
    
     
    janela.set_background_color((0,0,0))  
    l.draw()
    
    janela.update()

    
