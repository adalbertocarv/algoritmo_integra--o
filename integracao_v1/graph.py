from collections import defaultdict

def construir_grafo(paradas, linhas_de_onibus):
    grafo = defaultdict(list)
    for parada in paradas:
        for linha in linhas_de_onibus[parada]:
            for vizinha in paradas:
                if linha in linhas_de_onibus[vizinha] and vizinha != parada:
                    grafo[parada].append((vizinha, linha))
    return grafo
