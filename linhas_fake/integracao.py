from collections import deque, defaultdict

# Estruturas de Dados
# Lista de paradas de ônibus de 1 a 20
paradas = list(range(1, 21))  # Paradas de 1 a 20

# Dicionário onde a chave é a parada e o valor é uma lista de linhas de ônibus que passam por essa parada
linhas_de_onibus = defaultdict(list)

# Preenchendo o dicionário com linhas de ônibus para cada parada
# Usando sobreposição para garantir conectividade entre paradas
for i in range(1, 21):
    for j in range(i, i + 5):
        linhas_de_onibus[i].append(f'L{(j % 20) + 1}.{(j % 5) + 1}')

# Construção do grafo
# Dicionário onde a chave é uma parada e o valor é uma lista de tuplas (vizinha, linha)
# Representa as conexões diretas entre paradas e as linhas de ônibus que as conectam
grafo = defaultdict(list)

# Para cada parada, verificamos quais outras paradas compartilham linhas de ônibus
# Adicionamos arestas entre essas paradas no grafo
for parada in paradas:
    for linha in linhas_de_onibus[parada]:
        for vizinha in paradas:
            if linha in linhas_de_onibus[vizinha] and vizinha != parada:
                grafo[parada].append((vizinha, linha))

# Função para encontrar o caminho com integração entre linhas
# Utiliza Busca em Largura (BFS) para explorar o grafo
def encontrar_caminho_com_integracao(origem, destino):
    # Fila para BFS, armazenando (parada_atual, caminho_percorrido)
    fila = deque([(origem, [])])
    # Conjunto para evitar visitar a mesma parada mais de uma vez
    visitados = set()

    # Enquanto a fila não estiver vazia
    while fila:
        # Remove a parada atual da fila
        parada_atual, caminho = fila.popleft()

        # Se a parada atual é a parada de destino, retornamos o caminho encontrado
        if parada_atual == destino:
            return caminho + [parada_atual]

        # Se a parada atual não foi visitada
        if parada_atual not in visitados:
            # Marca a parada atual como visitada
            visitados.add(parada_atual)

            # Para cada vizinho da parada atual
            for vizinho, linha in grafo[parada_atual]:
                # Se o vizinho não foi visitado
                if vizinho not in visitados:
                    # Adiciona o vizinho à fila com o caminho atualizado
                    fila.append((vizinho, caminho + [parada_atual, linha]))

    # Se não encontramos um caminho, retornamos None
    return None

# Função para exibir todas as paradas com suas linhas
def exibir_paradas_e_linhas():
    # Para cada parada e suas linhas
    for parada, linhas in linhas_de_onibus.items():
        # Exibimos a parada e as linhas
        print(f"Parada {parada}: {', '.join(linhas)}")

# Função principal
def main():
    # Exibe todas as paradas com suas linhas
    exibir_paradas_e_linhas()

    # Solicita ao usuário a parada de origem
    origem = int(input("Digite a parada de origem (1-20): "))
    # Solicita ao usuário a parada de destino
    destino = int(input("Digite a parada de destino (1-20): "))

    # Encontra o caminho com integração entre linhas
    caminho = encontrar_caminho_com_integracao(origem, destino)

    # Se encontramos um caminho
    if caminho:
        print("Caminho encontrado:")
        # Para cada parada no caminho
        for i in range(0, len(caminho) - 1, 2):
            # Exibimos a parada, a linha e a próxima parada
            if i + 2 < len(caminho):
                print(f"Parada {caminho[i]} -> Linha {caminho[i + 1]} -> Parada {caminho[i + 2]}")
            else:
                print(f"Parada {caminho[i]} -> Linha {caminho[i + 1]} -> Parada {caminho[i + 2]}")

        # Se o caminho tem mais de 3 elementos, identificamos o ponto de integração
        if len(caminho) > 3:
            ponto_b = caminho[2]
            print(f"Ponto de integração: Parada {ponto_b}")
    else:
        # Se nenhum caminho foi encontrado
        print("Nenhum caminho encontrado.")

# Execução do script
if __name__ == "__main__":
    main()