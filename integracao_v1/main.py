from database import carregar_dados_bd
from graph import construir_grafo
from a_star import encontrar_caminho_com_integracao_astar
from utils import salvar_grafo, carregar_grafo

def main():
    caminho_bd = 'paradas_linhas.db'
    caminho_arquivo_grafo = 'grafo.pkl'
    
    grafo = carregar_grafo(caminho_arquivo_grafo)
    
    if grafo is None:
        paradas, linhas_de_onibus = carregar_dados_bd(caminho_bd)
        grafo = construir_grafo(paradas, linhas_de_onibus)
        salvar_grafo(grafo, caminho_arquivo_grafo)
    else:
        print("Grafo carregado a partir do arquivo.")
    
    while True:
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

if __name__ == "__main__":
    main()
