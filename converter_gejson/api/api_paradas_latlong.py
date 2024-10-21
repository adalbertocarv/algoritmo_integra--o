from fastapi import FastAPI, HTTPException
import sqlite3

app = FastAPI()

# Função para conectar ao banco de dados SQLite
def get_db_connection():
    conn = sqlite3.connect('geojson_data.db')
    conn.row_factory = sqlite3.Row  # Para retornar os dados como dicionário
    return conn

# Endpoint para buscar dados com base no codDftrans
@app.get("/parada/{codDftrans}")
def get_dados(codDftrans: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Consulta SQL para buscar dados com base no codDftrans
    cursor.execute("SELECT * FROM geojson_data WHERE codDftrans = ?", (codDftrans,))
    row = cursor.fetchone()
    
    # Fechar conexão
    conn.close()
    
    # Se não encontrar, retorna 404
    if row is None:
        raise HTTPException(status_code=404, detail="Dados não encontrados")
    
    # Montar o objeto GeoJSON com os dados
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
    
    return geojson

# Executar a aplicação usando o Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
