import sqlite3
from collections import defaultdict

def carregar_dados_bd(caminho_bd):
    conn = sqlite3.connect(caminho_bd)
    cursor = conn.cursor()
    
    # Dicionários para armazenar as paradas e linhas
    paradas = []
    linhas_de_onibus = defaultdict(list)
    
    cursor.execute('SELECT parada_id, linhas FROM paradas_linhas')
    for row in cursor.fetchall():
        parada_id = row[0]
        linhas = row[1].split(', ')
        paradas.append(parada_id)
        linhas_de_onibus[parada_id].extend(linhas)
    
    conn.close()
    return paradas, linhas_de_onibus