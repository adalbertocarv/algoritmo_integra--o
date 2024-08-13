import csv
import pickle
import os
from collections import deque, defaultdict

# Estruturas de Dados
paradas = []  # Lista de paradas de ônibus
linhas_de_onibus = defaultdict(list)  # Dicionário com as linhas por parada

# Caminho para o arquivo de cache
pickle_file = 'paradas_linhas.pkl'

# Função para carregar os dados do CSV
def carregar_dados_csv(caminho_arquivo):
    with open(caminho_arquivo, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            parada = int(row[0])  # Converte o código da parada para inteiro
            paradas.append(parada)  # Adiciona a parada à lista de paradas
            linhas = row[1].split(', ')  # Separa as linhas associadas à parada
            linhas_de_onibus[parada].extend(linhas)  # Adiciona as linhas ao dicionário

# Função para salvar os dados em um arquivo pickle
def salvar_dados_pickle():
    with open(pickle_file, 'wb') as f:
        pickle.dump((paradas, linhas_de_onibus), f)

# Função para carregar os dados de um arquivo pickle
def carregar_dados_pickle():
    with open(pickle_file, 'rb') as f:
        return pickle.load(f)

# Função para verificar se o cache existe e carregar os dados
def carregar_dados(caminho_arquivo):
    if os.path.exists(pickle_file):
        # Se o arquivo pickle existe, carrega os dados dele
        return carregar_dados_pickle()
    else:
        # Se não existe, carrega do CSV e salva no pickle
        carregar_dados_csv(caminho_arquivo)
        salvar_dados_pickle()
        return paradas, linhas_de_onibus

# Construção do grafo
grafo = defaultdict(list)

# Função para construir o grafo de conexões
def construir_grafo():
    for parada in paradas:
        for linha in linhas_de_onibus[parada]:
            for vizinha in paradas:
                if linha in linhas_de_onibus[vizinha] and vizinha != parada:
                    grafo[parada].append((vizinha, linha))

# Função para encontrar o caminho com integração entre linhas
def encontrar_caminho_com_integracao(origem, destino):
    fila = deque([(origem, [])])
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


# Função principal
def main():
    caminho_arquivo_csv = 'paradas_linhas.csv'
    
    # Carrega os dados do cache ou do CSV
    global paradas, linhas_de_onibus
    paradas, linhas_de_onibus = carregar_dados(caminho_arquivo_csv)

    # Constrói o grafo com base nos dados carregados
    construir_grafo()

    origem = int(input("Digite a parada de origem: "))
    destino = int(input("Digite a parada de destino: "))

    caminho = encontrar_caminho_com_integracao(origem, destino)

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

# Execução do script
if __name__ == "__main__":
    main()
