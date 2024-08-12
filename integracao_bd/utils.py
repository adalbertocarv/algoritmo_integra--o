def heuristic(parada_atual, parada_destino):
    # Implementar uma função que calcula a distância geográfica
    # Aqui usamos uma heurística simples, como distância euclidiana
    return calcular_distancia(parada_atual, parada_destino)

def calcular_distancia(parada_atual, parada_destino):
    # Usar a diferença entre os valores hash como uma heurística simples
    return abs(hash(parada_atual) - hash(parada_destino))

