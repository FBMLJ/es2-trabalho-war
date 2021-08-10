from telas.Cadastro import Cadastro
import pygame
from PPlay import window
from telas.Login import Login

janela = window.Window(1280,720)
l = Login(janela)


l.loop()