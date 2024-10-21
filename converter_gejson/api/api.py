from fastapi import FastAPI, HTTPException, Query
import sqlite3

app = FastAPI()

# Função para conectar ao banco de dados SQLite
def get_db_connection():
    conn = sqlite3.connect('geojson_data.db')
    conn.row_factory = sqlite3.Row  # Para retornar os dados como dicionário
    return conn

# Endpoint para buscar dados com base em múltiplos valores de codDftrans
@app.get("/paradas/")
def get_dados(codDftrans: list[str] = Query(...)):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Construir a consulta SQL com múltiplos valores de codDftrans
    query = f"SELECT * FROM geojson_data WHERE codDftrans IN ({','.join('?' * len(codDftrans))})"
    cursor.execute(query, codDftrans)
    
    rows = cursor.fetchall()
    conn.close()

    # Se nenhum dado for encontrado, retornar erro 404
    if not rows:
        raise HTTPException(status_code=404, detail="Nenhuma parada encontrada")

    # Montar a lista de objetos GeoJSON com os dados
    geojson_features = []
    for row in rows:
        geojson = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [row["longitude"], row["latitude"]]
            },
            "properties": {
                "sequencial": row["sequencial"],
                "sentido": row["sentido"],
                "codDftrans": row["codDftrans"]
            }
        }
        geojson_features.append(geojson)
    
    return {
        "type": "FeatureCollection",
        "features": geojson_features
    }

# Executar a aplicação usando o Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
