from telas.menuPrincipal import MenuPrincipal, TelaGeral

class ControleDeTelas:
    def __init__(self, pygame,screen, clock):
        self.tela_atual = "menu_principal"
        self.screen = screen
        self.pygame = pygame
        self.clock = clock
        self.telas = {"menu_principal": MenuPrincipal(self)}

    def trocaTela(self, novaTela):
        self.tela_atual = novaTela
    
    def exebirTelaAtual(self):
        if (self.telas[self.tela_atual]!= None):
            
            self.telas[self.tela_atual].exibir()
        else:
            print("Tela ainda não atribuida")
        
    def getTelaAtual(self):
        return  self.telas[self.tela_atual]
    
    def gameLoop(self):
        self.rodando = True
        while self.rodando:

            #apaga tudo do frame anterio
            self.screen.fill((255,255,255))
            self.exebirTelaAtual()

            #desenha tudo no novo frame
            self.pygame.display.flip()

            #limita fps em 60
            self.clock.tick(60)
        self.pygame.quit()
