from jogo.Territorio import Territorio
from jogo.Player import Player
from random import randint, shuffle

class BotGeral(Player):
    def __init__(self) -> None:
        super().__init__()
        '''
        self.territorios = []
        self.cartas = []
        self.tropas_pendentes = 0
        self.objetivo = None
        self.pode_jogar = False
        self.cor = ""
        '''
        self.bot = True
        #Listas para resetar no fim do turno
        self.cartas_a_trocar = []
        self.ataques_a_fazer = [] #[0]atacante, [1]defensor

    '''
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    O CardManager deve iterar pela lista de cartas a trocar e chamar sua funcao
    trocar cartas para esta lista de cartas
    '''

    '''
    Funcao que faz o Bot escolher as cartas para trocar
    Procura pelas cartas de quadrado
    Procura pelas cartas de triangulo
    Procura pelas cartas de circulo
    Se tiver 3 ou mais cartas com o mesmo simbolo, bota na lista de cartas para trocar
    Se tiver 3 cartas de simbolos diferentes, coloca na lista de cartas para trocar
    '''
    def escolhe_cartas_para_trocar(self) -> None:
        if len(self.cartas) < 3:
            return
        # Procura pelas cartas de quadrado
        cartas_quadrado = []
        for carta in self.cartas:
            if carta.figura == "Quadrado":
                cartas_quadrado.append(carta)
        # Procura pelas cartas de triangulo
        cartas_triangulo = []
        for carta in self.cartas:
            if carta.figura == "Triangulo":
                cartas_triangulo.append(carta)
        # Procura pelas cartas de circulo
        cartas_circulo = []
        for carta in self.cartas:
            if carta.figura == "Circulo":
                cartas_circulo.append(carta)
        # Se tiver 3 ou mais cartas com o mesmo simbolo, bota na lista de cartas para trocar
        if len(cartas_quadrado) >= 3:
            self.cartas_a_trocar.append(cartas_quadrado[0])
            self.cartas_a_trocar.append(cartas_quadrado[1])
            self.cartas_a_trocar.append(cartas_quadrado[2])
            return
        elif len(cartas_triangulo) >= 3:
            self.cartas_a_trocar.append(cartas_triangulo[0])
            self.cartas_a_trocar.append(cartas_triangulo[1])
            self.cartas_a_trocar.append(cartas_triangulo[2])
            return
        elif len(cartas_circulo) >= 3:
            self.cartas_a_trocar.append(cartas_circulo[0])
            self.cartas_a_trocar.append(cartas_circulo[1])
            self.cartas_a_trocar.append(cartas_circulo[2])
            return
        # Se tiver 3 cartas de simbolos diferentes, coloca na lista de cartas para trocar
        elif len(cartas_quadrado) >= 1 and len(cartas_triangulo) >= 1 and len(cartas_circulo) >= 1:
            self.cartas_a_trocar.append(cartas_quadrado[0])
            self.cartas_a_trocar.append(cartas_triangulo[0])
            self.cartas_a_trocar.append(cartas_circulo[0])
            return
        # Busca pelas cartas coringas
        cartas_coringa = []
        for carta in self.cartas:
            if carta.coringa:
                cartas_coringa.append(carta)
        if len(cartas_coringa) == 1:
            # Busca duas cartas nao coringas para participar da troca
            duas_cartas_para_achar = 2
            for carta in self.cartas:
                if not carta.coringa and duas_cartas_para_achar > 0:
                    duas_cartas_para_achar -= 1
                    self.cartas_a_trocar.append(carta)
            self.cartas_a_trocar.append(cartas_coringa[0])
        if len(cartas_coringa) == 2:
            # Busca duas cartas nao coringas para participar da troca
            duas_cartas_para_achar = 1
            for carta in self.cartas:
                if not carta.coringa and duas_cartas_para_achar > 0:
                    duas_cartas_para_achar -= 1
                    self.cartas_a_trocar.append(carta)
            self.cartas_a_trocar.append(cartas_coringa[0])
            self.cartas_a_trocar.append(cartas_coringa[1])
        return
 
    def distribuir_tropas(self) -> None:
        escolha = randint(0,1)
        if escolha:
            self.distribui_igual()
        else:
            self.distribui_aleatorio()
    
    '''
    Funcao que faz o bot distribuir suas tropas
    Embaralha a lista de territorios, e coloca 1 tropa em cada ciclicamente.
    '''
    def distribui_igual(self):
        #Embaralha a lista de territorios
        shuffle(self.territorios)
        #Coloca 1 tropa em cada ciclicamente.
        tropas_a_distribuir = self.tropas_pendentes
        i = 0
        for _ in range(tropas_a_distribuir):
            self.tropas_pendentes -= 1
            self.territorios[i].recebe_tropas(1)
            i += 1
            if i >= len(self.territorios):
                i = 0
        return

    #Distribui aleatoriamente tropas entre os territorios
    def distribui_aleatorio(self) -> None:
        shuffle(self.territorios)
        #Quantidade total de tropas a serem distribuidas
        tropas_a_distribuir = self.tropas_pendentes
        
        i = 0
        while tropas_a_distribuir > 0:
            tropas_enviadas = randint(1, tropas_a_distribuir)
            tropas_a_distribuir -= tropas_enviadas
            self.territorios[i].recebe_tropas(tropas_enviadas)
            i += 1
        return
    '''
    @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    O CombateManager deve iterar pela lista de ataques_a_fazer e chamar sua funcao
    atacar para cada um destes territorios
    '''

    '''
    Funcao que escolhe onde atacar e quantas vezes
    Embaralha a lista de territorios
    Seleciona os territorios com tropas o suficiente para ser o atacante
    Procura pelos territorios vizinhos que o bot nao tem
    Adiciona na lista de territorios para atacar, o atacante[0] e o vizinho[1]
    '''
    def escolhe_atacar(self):
        #Embaralha a lista de territorios
        shuffle(self.territorios)
        #Seleciona os territorios com tropas o suficiente para ser o atacante
        territorios_com_tropas_para_atacar = (t for t in self.territorios if t.quantidade_tropas > 1)
        for territorio in territorios_com_tropas_para_atacar:
            #Procura pelos territorios vizinhos que o bot nao tem
            for vizinho in territorio.vizinho:
                if vizinho not in self.territorios:
                    #Adiciona na lista de ataques a fazer
                    ataque = []
                    ataque.append(territorio)
                    ataque.append(vizinho)
                    self.ataques_a_fazer.append(ataque)
        return

    '''
    Funcao que desloca as tropas do bot
    Para cada territorio do bot
        Para cada vizinho deste territorio
            Verifica se encontrou um vizinho que nao esta na lista de territorios do bot
            Se nao encontrou, adiciona o territorio na lista de territorios sem vizinho inimigo
    Para cada territorio sem pelo menos 1 vizinho inimigo
        Embaralha a lista de vizinhos
        Verifica se tem tropas o suficiente para deslocar
        Desloca as tropas
    '''
    def deslocar_tropas(self):
        territorios_sem_vizinhos_inimigos = []
        #Para cada territorio do bot
        for territorio in self.territorios:
            tem_vizinho_inimigo = False
            #Para cada vizinho deste territorio
            for viz_itr in territorio.vizinho:
                #Verifica se encontrou um vizinho que nao esta na lista de territorios do bot
                if viz_itr not in self.territorios:
                    tem_vizinho_inimigo = True
            #Se nao encontrou, adiciona o territorio na lista de territorios sem vizinho inimigo
            if not tem_vizinho_inimigo:
                territorios_sem_vizinhos_inimigos.append(territorio)
        for ter_itr in territorios_sem_vizinhos_inimigos:
            #Embaralha a lista de vizinhos
            shuffle(ter_itr.vizinho)
            #Verifica se tem tropas o suficiente para deslocar
            tropas_a_deslocar = ter_itr.quantidade_tropas - ter_itr.tropas_deslocadas - 1
            if(tropas_a_deslocar > 0):
                #Desloca as tropas
                ter_itr.vizinho[0].recebe_tropas(tropas_a_deslocar)
                ter_itr.vizinho[0].tropas_deslocadas = tropas_a_deslocar
                ter_itr.perde_tropas(tropas_a_deslocar)
        return
