from PPlay.window import Window
from PPlay.mouse import Mouse
from telas.ControladorMapa import ControladorMapa
from constant import *

janela = Window(1366, 768)
mouse = Mouse()
controleMapa = ControladorMapa(janela)
janela.clear()
while True:
    teritorio_selecionado = controleMapa.selecionar_territorio(mouse)
    controleMapa.render()
    janela.update()