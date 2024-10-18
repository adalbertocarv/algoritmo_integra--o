from fastapi import FastAPI, HTTPException
from database import carregar_dados_bd
from graph import construir_grafo
from a_star import encontrar_caminho_com_integracao_astar
from utils import carregar_grafo, salvar_grafo

app = FastAPI()

caminho_bd = 'paradas_linhas.db'
caminho_arquivo_grafo = 'grafo.pkl'

# Carrega ou constrói o grafo na inicialização
grafo = carregar_grafo(caminho_arquivo_grafo)
if grafo is None:
    paradas, linhas_de_onibus = carregar_dados_bd(caminho_bd)
    grafo = construir_grafo(paradas, linhas_de_onibus)
    salvar_grafo(grafo, caminho_arquivo_grafo)

@app.get("/rotas/")
def obter_rota(origem: int, destino: int):
    caminho = encontrar_caminho_com_integracao_astar(grafo, origem, destino)
    
    if not caminho:
        raise HTTPException(status_code=404, detail="Nenhuma rota encontrada")
    
    rota_detalhada = []
    for i in range(0, len(caminho) - 1, 2):
        rota_detalhada.append({
            "parada_origem": caminho[i],
            "linha": caminho[i + 1],
            "parada_destino": caminho[i + 2] if i + 2 < len(caminho) else caminho[i]
        })
    
    return {"rota": rota_detalhada}

@app.get("/paradas/")
def listar_paradas():
    paradas, linhas_de_onibus = carregar_dados_bd(caminho_bd)
    return {"paradas": paradas, "linhas": linhas_de_onibus}
