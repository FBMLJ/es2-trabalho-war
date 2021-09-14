from random import shuffle

class BotGeral:
    def __init__(self) -> None:
        self.territorios = []
        self.cartas = []
        self.tropas_pendentes = 0
        self.objetivo = None
        self.pode_jogar = False
        self.cor = ""
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
        #Procura pelas cartas de quadrado
        cartas_quadrado = (c for c in self.cartas if c.figura == "QUADRADO")
        #Procura pelas cartas de triangulo
        cartas_triangulo = (c for c in self.cartas if c.figura == "TRIANGULO")
        #Procura pelas cartas de circulo
        cartas_circulo = (c for c in self.cartas if c.figura == "CIRCULO")
        # Se tiver 3 ou mais cartas com o mesmo simbolo, bota na lista de cartas para trocar
        if(len(cartas_quadrado) >= 3):
            self.cartas_a_trocar.append(cartas_quadrado[0])
            self.cartas_a_trocar.append(cartas_quadrado[1])
            self.cartas_a_trocar.append(cartas_quadrado[2])
        elif(len(cartas_triangulo) >= 3):
            self.cartas_a_trocar.append(cartas_triangulo[0])
            self.cartas_a_trocar.append(cartas_triangulo[1])
            self.cartas_a_trocar.append(cartas_triangulo[2])
        elif(len(cartas_circulo) >= 3):
            self.cartas_a_trocar.append(cartas_circulo[0])
            self.cartas_a_trocar.append(cartas_circulo[1])
            self.cartas_a_trocar.append(cartas_circulo[2])
        #Se tiver 3 cartas de simbolos diferentes, coloca na lista de cartas para trocar
        elif len(cartas_quadrado) >= 1 and len(cartas_triangulo) >= 1 and len(cartas_circulo) >= 1:
            self.cartas_a_trocar.append(cartas_quadrado[0])
            self.cartas_a_trocar.append(cartas_triangulo[0])
            self.cartas_a_trocar.append(cartas_circulo[0])
        return

    '''
    Funcao que faz o bot distribuir suas tropas
    Embaralha a lista de territorios, e coloca 1 tropa em cada ciclicamente.
    '''
    def distribuir_tropas(self) -> None:
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

    def deslocar_tropas(self):
        return
