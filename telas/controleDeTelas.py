class ControleDeTelas:
    def __init__(self):
        self.telas = {"menu_principal": None}
        self.tela_atual = "menu_principal"

    def trocaTela(self, novaTela):
        self.tela_atual = novaTela
    
    def exebirTelaAtual(self):
        if (self.telas[self.tela_atual]!= None):
            self.telas[self.tela_atual].exibir()
        else:
            print("Tela ainda não atribuida")
        
    def getTelaAtual(self):
        return  self.telas[self.tela_atual]