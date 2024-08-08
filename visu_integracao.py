from collections import deque, defaultdict
import networkx as nx
import matplotlib.pyplot as plt

# Estruturas de Dados
paradas = list(range(1, 21))  # Paradas de 1 a 20
linhas_de_onibus = defaultdict(list)

# Preenchendo linhas de ônibus para cada parada com sobreposição para garantir conectividade
for i in range(1, 21):
    for j in range(i, i + 5):
        linhas_de_onibus[i].append(f'L{(j % 20) + 1}.{(j % 5) + 1}')

# Construção do grafo
grafo = defaultdict(list)

for parada in paradas:
    for linha in linhas_de_onibus[parada]:
        for vizinha in paradas:
            if linha in linhas_de_onibus[vizinha] and vizinha != parada:
                grafo[parada].append((vizinha, linha))

# Função para encontrar o caminho com integração entre linhas
def encontrar_caminho_com_integracao(origem, destino):
    fila = deque([(origem, [])])  # Fila para BFS, armazenando (parada_atual, caminho_percorrido)
    visitados = set()

    while fila:
        parada_atual, caminho = fila.popleft()

        if parada_atual == destino:
            return caminho + [parada_atual]

        if parada_atual not in visitados:
            visitados.add(parada_atual)

            for vizinho, linha in grafo[parada_atual]:
                if vizinho not in visitados:
                    fila.append((vizinho, caminho + [parada_atual, linha]))

    return None

# Função para exibir todas as paradas com suas linhas
def exibir_paradas_e_linhas():
    for parada, linhas in linhas_de_onibus.items():
        print(f"Parada {parada}: {', '.join(linhas)}")

# Função para desenhar o grafo
def desenhar_grafo(grafo):
    G = nx.Graph()

    # Adicionando nós e arestas ao grafo
    for parada, vizinhos in grafo.items():
        for vizinho, linha in vizinhos:
            G.add_edge(parada, vizinho, label=linha)

    pos = nx.spring_layout(G)  # Layout do grafo
    plt.figure(figsize=(12, 8))

    # Desenhando o grafo
    nx.draw(G, pos, with_labels=True, node_size=5000, node_color='lightblue', font_size=10, font_weight='bold', edge_color='gray')
    labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_color='red')

    plt.title("Grafo de Conexões entre Paradas e Linhas de Ônibus")
    plt.show()

# Função principal
def main():
    exibir_paradas_e_linhas()

    origem = int(input("Digite a parada de origem (1-20): "))
    destino = int(input("Digite a parada de destino (1-20): "))

    caminho = encontrar_caminho_com_integracao(origem, destino)

    if caminho:
        print("Caminho encontrado:")
        for i in range(0, len(caminho) - 1, 2):
            if i + 2 < len(caminho):
                print(f"Parada {caminho[i]} -> Linha {caminho[i + 1]} -> Parada {caminho[i + 2]}")
            else:
                print(f"Parada {caminho[i]} -> Linha {caminho[i + 1]} -> Parada {caminho[i + 2]}")

        if len(caminho) > 3:
            ponto_b = caminho[2]
            print(f"Ponto de integração: Parada {ponto_b}")
    else:
        print("Nenhum caminho encontrado.")

    # Desenhar o grafo
    desenhar_grafo(grafo)

# Execução do script
if __name__ == "__main__":
    main()
