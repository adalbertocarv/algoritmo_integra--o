import pickle

def salvar_grafo(grafo, caminho_arquivo='grafo.pkl'):
    """Salva o grafo em um arquivo usando pickle."""
    with open(caminho_arquivo, 'wb') as f:
        pickle.dump(grafo, f)

def carregar_grafo(caminho_arquivo='grafo.pkl'):
    """Carrega o grafo de um arquivo usando pickle."""
    try:
        with open(caminho_arquivo, 'rb') as f:
            grafo = pickle.load(f)
        return grafo
    except FileNotFoundError:
        return None
