

class TelaGeral:
    

    def __init__(self,pygame):
        self.pygame =  pygame

    def exibir(self):
        self.trataEvento()

    def eventoPadrao(self,event):
        if event.type == self.pygame.QUIT:
            exit()
    
    def eventoDaTela(self,event):
        pass

    def trataEvento(self):
        for event in self.pygame.event.get():
            self.eventoPadrao(event)
            self.eventoDaTela(event)
