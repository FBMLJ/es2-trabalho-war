from componentes.campoTexto import *
from PPlay.gameimage import *
from PPlay.sprite import *
from componentes.botao import *
from componentes.campoSenha import *
import pygame

'''
Classe para definir o componente de popup de senha para entrar e saguao
'''
class SenhaPopUp:
    # Inicia o objeto com seus respectivos sprites, fundo e inputs nas posicoes corretas
    def __init__(self, janela):
        
        self.janela = janela
        
        self.fundo = GameImage("assets/imagem/busca_saguao/sombra.png")

        self.popup_box = GameImage("assets/imagem/busca_saguao/popup.png")
        self.popup_box.set_position(
            janela.width/2 - self.popup_box.width/2,
            self.janela.height/2 - self.popup_box.height/2            
        )

        self.input = CampoSenha(
            janela,
            GameImage("assets/imagem/busca_saguao/senha_da_sala.png"), 
            self.popup_box.x + 40, 
            self.popup_box.y + 52,
            250,
            40, 
            22
        )

        self.entrar_botao = Botao(
            Sprite("assets/imagem/busca_saguao/botao_entrar.png"),
            Sprite("assets/imagem/busca_saguao/botao_entrar_select.png"),
            1
        )
        self.entrar_botao.setposition(
            self.popup_box.x + self.popup_box.width/2 - self.entrar_botao.width/2,
            self.popup_box.y + self.popup_box.height - 45
        )
        
        self.fechar_botao = Botao(
            Sprite("assets/imagem/busca_saguao/x_popup.png"),
            Sprite("assets/imagem/busca_saguao/x_popup.png"),
            2
        )
        self.fechar_botao.setposition(
            self.popup_box.x + self.popup_box.width - self.fechar_botao.width - 5,
            self.popup_box.y + 5
        )

    #Atualiza os componentes do popup a cada frame
    def update(self):
        self.trataEventos()
        update_botao = self.entrar_botao.update()
        if(update_botao):
            return self.entrar_botao.code
        update_fechar = self.fechar_botao.update()
        if(update_fechar):
            return self.fechar_botao.code
        #Codigo padrao de que nao houve eventos
        return 0

    #Renderiza os objetos do popup
    def render(self):
        self.fundo.draw()
        self.popup_box.draw()
        self.input.draw()
        self.entrar_botao.render()
        self.fechar_botao.render()
    
    def trataEventos(self):
        for evento in pygame.event.get():
            self.input.evento(evento)
            if evento.type == pygame.QUIT:
                exit()

    
    
        