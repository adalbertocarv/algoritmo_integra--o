from database import connect_to_db, fetch_paradas_e_linhas
from graph import build_graph
from a_star import a_star_search

def main(origem, destino):
    conn = connect_to_db()
    if conn:
        results = fetch_paradas_e_linhas(conn)
        conn.close()

        graph = build_graph(results)
        caminho = a_star_search(graph, origem, destino)
        
        if caminho != "No Path Found":
            for parada, linha in caminho:
                print(f"Pegar linha {linha} na parada {parada}")
        else:
            print("Nenhuma rota encontrada.")
    else:
        print("Falha na conexão com o banco de dados.")

if __name__ == "__main__":
    origem = '1235'  # Insira o código da parada de origem
    destino = '3447'  # Insira o código da parada de destino
    main(origem, destino)
