import sqlite3
import csv

def criar_bd_e_popular(caminho_bd, caminho_csv):
    # Conecta ao banco de dados (ou cria se não existir)
    conn = sqlite3.connect(caminho_bd)
    cursor = conn.cursor()

    # Cria a tabela de paradas e linhas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS paradas_linhas (
        parada_id INTEGER PRIMARY KEY,
        linhas TEXT
    )
    ''')

    # Lê o CSV e insere os dados no banco
    with open(caminho_csv, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            parada_id = int(row[0])
            linhas = row[1]
            cursor.execute('''
            INSERT OR REPLACE INTO paradas_linhas (parada_id, linhas)
            VALUES (?, ?)
            ''', (parada_id, linhas))

    # Salva as mudanças e fecha a conexão
    conn.commit()
    conn.close()

# Exemplo de uso
caminho_bd = 'paradas_linhas.db'
caminho_csv = 'paradas_linhas.csv'
criar_bd_e_popular(caminho_bd, caminho_csv)
