def heuristic(parada_atual, parada_destino):
    # Implementar uma função que calcula a distância geográfica
    # Aqui usamos uma heurística simples, como distância euclidiana
    return calcular_distancia(parada_atual, parada_destino)

def calcular_distancia(parada_atual, parada_destino):
    # Exemplo simples de cálculo de distância, pode ser substituído por algo mais complexo
    return abs(parada_atual - parada_destino)
