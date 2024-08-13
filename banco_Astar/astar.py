import sqlite3
import heapq
from collections import defaultdict

# Função para carregar os dados das paradas e linhas do banco de dados SQLite
def carregar_dados_bd(caminho_bd):
    conn = sqlite3.connect(caminho_bd)
    cursor = conn.cursor()
    
    # Dicionários para armazenar as paradas e linhas
    paradas = []
    linhas_de_onibus = defaultdict(list)
    
    cursor.execute('SELECT parada_id, linhas FROM paradas_linhas')
    for row in cursor.fetchall():
        parada_id = row[0]
        linhas = row[1].split(', ')
        paradas.append(parada_id)
        linhas_de_onibus[parada_id].extend(linhas)
    
    conn.close()
    return paradas, linhas_de_onibus

# Função heurística simples (número de trocas mínimas)
def heuristica(parada_atual, destino):
    return abs(parada_atual - destino)

# Função A* para encontrar o caminho mais eficiente entre duas paradas
def encontrar_caminho_com_integracao_astar(grafo, origem, destino):
    fila = [(0, origem, [])]  # (custo_total, parada_atual, caminho)
    visitados = set()

    while fila:
        custo, parada_atual, caminho = heapq.heappop(fila)

        if parada_atual == destino:
            return caminho + [parada_atual]

        if parada_atual not in visitados:
            visitados.add(parada_atual)

            for vizinho, linha in grafo[parada_atual]:
                if vizinho not in visitados:
                    custo_estimado = custo + 1 + heuristica(vizinho, destino)
                    heapq.heappush(fila, (custo_estimado, vizinho, caminho + [parada_atual, linha]))

    return None

# Função para construir o grafo de conexões
def construir_grafo(paradas, linhas_de_onibus):
    grafo = defaultdict(list)
    for parada in paradas:
        for linha in linhas_de_onibus[parada]:
            for vizinha in paradas:
                if linha in linhas_de_onibus[vizinha] and vizinha != parada:
                    grafo[parada].append((vizinha, linha))
    return grafo

# Exemplo de como chamar a função A*
def main():
    caminho_bd = 'paradas_linhas.db'

    # Carrega os dados do banco de dados
    paradas, linhas_de_onibus = carregar_dados_bd(caminho_bd)

    # Constrói o grafo com base nos dados carregados
    grafo = construir_grafo(paradas, linhas_de_onibus)

    origem = int(input("Digite a parada de origem: "))
    destino = int(input("Digite a parada de destino: "))

    caminho = encontrar_caminho_com_integracao_astar(grafo, origem, destino)

    if caminho:
        print("Caminho encontrado:")
        for i in range(0, len(caminho) - 1, 2):
            if i + 2 < len(caminho):
                print(f"Parada {caminho[i]} -> Linha {caminho[i + 1]} -> Parada {caminho[i + 2]}")
            else:
                print(f"Parada {caminho[i]} -> Linha {caminho[i + 1]} -> Parada {caminho[i + 2]}")

        if len(caminho) > 3:
            ponto_c = caminho[2]
            print(f"Ponto de integração: Parada {ponto_c}")
    else:
        print("Nenhum caminho encontrado.")

# Executar a função principal
if __name__ == "__main__":
    main()
