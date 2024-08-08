import json

# Carregar o JSON de um arquivo
with open('paradas.json', 'r', encoding='utf-8') as file:
    data = json.load(file)



# Verificar se 'data' contém a chave 'features'
if 'features' not in data or not isinstance(data['features'], list):
    raise ValueError("O JSON deve conter uma lista de objetos na chave 'features'.")

# Número total de objetos antes da filtragem
total_objetos_antes = len(data['features'])

# Listas para armazenar os dados filtrados e removidos
filtered_data = []
removed_data = []

# Filtrar os itens com "sentido": null e separar os removidos
for item in data['features']:
    if item['properties']['sentido'] is not None:
        filtered_data.append(item)
    else:
        removed_data.append(item)

# Número total de objetos após a filtragem
total_objetos_depois = len(filtered_data)

# Calcular o número de objetos removidos
objetos_removidos = total_objetos_antes - total_objetos_depois

# Atualizar a chave 'features' com os dados filtrados
data['features'] = filtered_data

# Converter o resultado de volta para JSON
result_json = json.dumps(data, indent=4)

# Salvar o JSON filtrado de volta no arquivo
with open('dados_filtrados.json', 'w', encoding='utf-8') as file:
    file.write(result_json)

# Converter os dados removidos para JSON
removed_json = json.dumps({'features': removed_data}, indent=4)

# Salvar os dados removidos em um arquivo separado
with open('dados_removidos.json', 'w', encoding='utf-8') as file:
    file.write(removed_json)

print(f"Objetos com 'sentido': null foram removidos: {objetos_removidos}.")
print("Os dados filtrados foram salvos em 'dados_filtrados.json'.")
print("Os dados removidos foram salvos em 'dados_removidos.json'.")
