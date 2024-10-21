import sqlite3

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('geojson_data.db')
cursor = conn.cursor()

# Fazer uma consulta para acessar todos os dados da tabela
cursor.execute('SELECT * FROM geojson_data')

# Recuperar todos os resultados da consulta
rows = cursor.fetchall()

# Exibir os dados
for row in rows:
    print(f'Sequencial: {row[0]}, Sentido: {row[1]}, codDftrans: {row[2]}, Longitude: {row[3]}, Latitude: {row[4]}')

# Fechar a conexão
conn.close()
