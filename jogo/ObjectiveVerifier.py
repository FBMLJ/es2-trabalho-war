class ObjectiveVerifier:
    def __init__(self) -> None:
        pass

    '''
    Funcao para filtrar os objetivos que sao de destruir jogadores que nao estao na partida
    Primeiro pega as cores dos jogadores na partida
    Depois adiciona os objetivos que nao envolvem destruir um jogador de cor faltante
    '''
    def filtrar(self, objetivos: list, jogadores: list) -> list:
        #Primeiro pega as cores dos jogadores na partida
        cores_dos_jogadores = []
        for jog in jogadores:
            cores_dos_jogadores.append(jog.cor)
        #Depois adiciona os objetivos que nao envolvem destruir um jogador de cor faltante
        objetivos_filtrados = []
        for obj in objetivos:
            if obj.cor_a_destruir not in cores_dos_jogadores:
                objetivos_filtrados.append(obj)
        return objetivos_filtrados