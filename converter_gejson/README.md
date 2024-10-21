Aqui está a documentação detalhada do que foi desenvolvido para converter um arquivo GeoJSON em uma tabela SQLite e disponibilizar os dados por meio de uma API FastAPI, com retorno no formato GeoJSON:

---

## **Documentação do Projeto: Conversão de GeoJSON para SQLite e Disponibilização via API FastAPI**

### **Visão Geral**

Este projeto tem como objetivo:
1. **Converter um arquivo GeoJSON** para um banco de dados SQLite local.
2. **Disponibilizar uma API FastAPI** para consultar esses dados, retornando-os no formato GeoJSON.

#### **Ferramentas Utilizadas**:
- **Python 3.x**: Linguagem principal.
- **SQLite**: Banco de dados local leve.
- **FastAPI**: Framework para construção da API.
- **Uvicorn**: Servidor ASGI para rodar o FastAPI.

---

### **1. Conversão de GeoJSON para SQLite**

#### **Objetivo**
Carregar um arquivo GeoJSON que contém pontos geográficos (com coordenadas e propriedades) e armazenar essas informações em uma tabela SQLite para facilitar a consulta.

#### **Exemplo de GeoJSON utilizado**:

```json
{
    "features": [
        {
            "geometry": {
                "coordinates": [-47.959784, -15.880183],
                "type": "Point"
            },
            "type": "Feature",
            "properties": {
                "sequencial": 6543,
                "sentido": "BAIRRO-CENTRO",
                "codDftrans": "7006"
            }
        },
        {
            "geometry": {
                "coordinates": [-48.114039, -15.809688],
                "type": "Point"
            },
            "type": "Feature",
            "properties": {
                "sequencial": 2787,
                "sentido": "BAIRRO-CENTRO",
                "codDftrans": "1511"
            }
        }
    ],
    "type": "FeatureCollection"
}
```

#### **Passos para conversão**:

##### **1.1 Script Python para carregar GeoJSON e inserir no SQLite**

```python
import sqlite3
import json

# Carregar o GeoJSON
geojson_data = '''
{
    "features": [
        {
            "geometry": {
                "coordinates": [-47.959784, -15.880183],
                "type": "Point"
            },
            "type": "Feature",
            "properties": {
                "sequencial": 6543,
                "sentido": "BAIRRO-CENTRO",
                "codDftrans": "7006"
            }
        },
        {
            "geometry": {
                "coordinates": [-48.114039, -15.809688],
                "type": "Point"
            },
            "type": "Feature",
            "properties": {
                "sequencial": 2787,
                "sentido": "BAIRRO-CENTRO",
                "codDftrans": "1511"
            }
        }
    ],
    "type": "FeatureCollection"
}
'''

# Converter a string GeoJSON para um dicionário Python
geojson_dict = json.loads(geojson_data)

# Conectar ao banco de dados SQLite (ou criar um novo)
conn = sqlite3.connect('geojson_data.db')
cursor = conn.cursor()

# Criar uma tabela SQLite
cursor.execute('''
CREATE TABLE IF NOT EXISTS geojson_data (
    sequencial INTEGER,
    sentido TEXT,
    codDftrans TEXT,
    longitude REAL,
    latitude REAL
)
''')

# Inserir dados na tabela
for feature in geojson_dict['features']:
    sequencial = feature['properties']['sequencial']
    sentido = feature['properties']['sentido']
    codDftrans = feature['properties']['codDftrans']
    longitude, latitude = feature['geometry']['coordinates']
    
    cursor.execute('''
    INSERT INTO geojson_data (sequencial, sentido, codDftrans, longitude, latitude)
    VALUES (?, ?, ?, ?, ?)
    ''', (sequencial, sentido, codDftrans, longitude, latitude))

# Salvar as mudanças
conn.commit()

# Fechar a conexão
conn.close()

print("Dados inseridos com sucesso na tabela SQLite.")
```

---

### **2. API FastAPI para disponibilização dos dados em GeoJSON**

#### **Objetivo**
Criar uma API usando FastAPI para consultar os dados armazenados no banco de dados SQLite, permitindo que os dados sejam consultados com base no campo `codDftrans` e retornados no formato GeoJSON.

#### **Instalação de Dependências**

Para rodar o FastAPI e o Uvicorn, é necessário instalar os pacotes via `pip`:

```bash
pip install fastapi uvicorn
```

#### **Estrutura da API**

##### **2.1 Código da API com FastAPI**

```python
from fastapi import FastAPI, HTTPException
import sqlite3

app = FastAPI()

# Função para conectar ao banco de dados SQLite
def get_db_connection():
    conn = sqlite3.connect('geojson_data.db')
    conn.row_factory = sqlite3.Row  # Para retornar os dados como dicionário
    return conn

# Endpoint para buscar dados com base no codDftrans
@app.get("/dados/{codDftrans}")
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
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

##### **2.2 Explicação dos Componentes**

- **Conexão com SQLite**: A função `get_db_connection()` estabelece a conexão com o banco de dados SQLite e define o `row_factory` para que os resultados sejam retornados como dicionários.
  
- **Rota `/dados/{codDftrans}`**: Esse endpoint permite que os usuários façam consultas no banco de dados usando o valor do campo `codDftrans` como parâmetro. O valor é então usado em uma consulta SQL.

- **Retorno em GeoJSON**: A consulta SQL retorna os dados associados ao `codDftrans` especificado, e esses dados são estruturados no formato GeoJSON.

##### **2.3 Execução da API**

Para rodar a API, use o comando abaixo:

```bash
uvicorn nome_do_arquivo:app --reload
```

A API estará disponível em `http://127.0.0.1:8000`.

---

### **3. Testes e Uso da API**

#### **Exemplo de Requisição**

Para consultar um dado com o `codDftrans = "7006"`, acesse a URL:

```
http://127.0.0.1:8000/dados/7006
```

#### **Exemplo de Resposta**

A resposta da API será no formato GeoJSON:

```json
{
    "type": "Feature",
    "geometry": {
        "type": "Point",
        "coordinates": [-47.959784, -15.880183]
    },
    "properties": {
        "sequencial": 6543,
        "sentido": "BAIRRO-CENTRO",
        "codDftrans": "7006"
    }
}
```

---

### **4. Conclusão**

Este projeto exemplifica como transformar dados geoespaciais no formato GeoJSON em uma tabela de banco de dados SQLite e como disponibilizar esses dados em uma API acessível, retornando-os no formato GeoJSON, utilizando FastAPI.

Essas ferramentas fornecem uma solução rápida, leve e eficiente para trabalhar com dados geoespaciais em Python, facilitando consultas e a integração com sistemas de terceiros.

---
## **Documentação Curta: Consulta de Múltiplos `codDftrans`**

### **Descrição**
Essa atualização permite consultar múltiplas paradas de ônibus simultaneamente, utilizando o campo `codDftrans` como parâmetro na URL. A API retorna os dados no formato GeoJSON para todos os pontos encontrados que correspondem aos valores fornecidos de `codDftrans`.

### **Requisição**

A API agora aceita múltiplos valores para `codDftrans` como query parameters na URL.

#### **Exemplo de URL**
```
http://127.0.0.1:8000/dados/?codDftrans=4973&codDftrans=3293
```

### **Resposta**

A resposta será um GeoJSON `FeatureCollection` contendo todos os pontos correspondentes aos valores fornecidos de `codDftrans`.

#### **Exemplo de Resposta**
```json
{
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [-47.959784, -15.880183]
            },
            "properties": {
                "sequencial": 6543,
                "sentido": "BAIRRO-CENTRO",
                "codDftrans": "4973"
            }
        },
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [-48.114039, -15.809688]
            },
            "properties": {
                "sequencial": 2787,
                "sentido": "BAIRRO-CENTRO",
                "codDftrans": "3293"
            }
        }
    ]
}
```

### **Notas**
- A API aceita múltiplos valores de `codDftrans` utilizando query strings (`?codDftrans=valor1&codDftrans=valor2`).
- O retorno é sempre um objeto GeoJSON no formato `FeatureCollection`, contendo todas as paradas que correspondem aos valores fornecidos.

---

Isso permite consultas eficientes e consolidadas de várias paradas ao mesmo tempo.