from ..jogo import Continente
from ..jogo import Territorio

class ControladorMapa:

    caminho_img_territorios = "..assets/imagem/mapa/territorios/"
    dicionario_territorios = {
        "Congo": 1,
        "Sudao": 2,
        "Egito": 3,
        "Madagascar": 4,
        "Argelia": 5,
        "Africa do Sul": 6,
        "Alaska":7,
        "Alberta":8,
        "Mexico":9,
        "Nova Iorque":10,
        "Groenlandia":11,
        "Mackenzie":12,
        "Ottawa":13,
        "Labrador":14,
        "California":15,
        "Argentina":16,
        "Brasil":17,
        "Peru":18,
        "Venezuela":19,
        "Aral":20,
        "China":21,
        "India":22,
        "Tchita":23,
        "Japao":24,
        "Vladivostok":25,
        "Oriente Medio":26,
        "Mongolia":27,
        "Vietna":28,
        "Dudinka":29,
        "Omsk":30,
        "Siberia":31,
        "Reino Unido":32,
        "Islandia":33,
        "Alemanha":34,
        "Escandinavia":35,
        "Italia":36,
        "Moscou":37,
        "Franca":38,
        "Australia Oriental":39,
        "Sumatra":40,
        "Nova Guine":41,
        "Australia Ocidental":42
    }

    def __init__(self, lista_continentes):
        self.continentes = lista_continentes

    def inicia_mapa(self):
        
        territorios_africa = []
        territorios_an = []
        territorios_as = []
        territorios_asia = []
        territorios_eu = []
        territorios_oc = []

        for territorio in self.dicionario_territorios:
            valor_territorio = self.dicionario_territorios[territorio]
            if valor_territorio <= 6:
                territorios_africa.append(Territorio(territorio, self.caminho_img_territorios + str(valor_territorio)))
            if valor_territorio > 6 and valor_territorio <= 15:
                territorios_an.append(Territorio(territorio, self.caminho_img_territorios + str(valor_territorio)))
            if valor_territorio > 6 and valor_territorio <= 19:
                territorios_as.append(Territorio(territorio, self.caminho_img_territorios + str(valor_territorio)))
            if valor_territorio > 19 and valor_territorio <= 31:
                territorios_asia.append(Territorio(territorio, self.caminho_img_territorios + str(valor_territorio)))
            if valor_territorio > 31 and valor_territorio <= 38:
                territorios_eu.append(Territorio(territorio, self.caminho_img_territorios + str(valor_territorio)))
            if valor_territorio > 38 and valor_territorio <= 42:
                territorios_oc.append(Territorio(territorio, self.caminho_img_territorios + str(valor_territorio)))
            else:
                print("Territorio nao reconhecido")
                return False