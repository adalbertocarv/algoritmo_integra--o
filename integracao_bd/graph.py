from collections import defaultdict

def build_graph(results):
    graph = defaultdict(list)
    for row in results:
        parada = row[0]  # cod_parada_dftrans
        linha = row[4]   # cod_linha
        destino = row[2] # geo_ponto_rede_pto
        
        # Adiciona a conexão no grafo
        graph[parada].append((linha, destino))
    return graph
