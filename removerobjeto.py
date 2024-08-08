import json

# Carregar o JSON de um arquivo
with open('paradas.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# Verificar o tipo de 'data' e salvar seu conteúdo para depuração
with open('dados_original.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4)

# Verificar se 'data' contém a chave 'features'
if 'features' not in data or not isinstance(data['features'], list):
    raise ValueError("O JSON deve conter uma lista de objetos na chave 'features'.")

# Número total de objetos antes da filtragem
total_objetos_antes = len(data['features'])

# Filtrar os itens com "sentido": null
filtered_data = [item for item in data['features'] if item['properties']['sentido'] is not None]

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


print(f"Objetos com 'sentido': null foram removidos: {objetos_removidos}.")
print("Os dados filtrados foram salvos em 'dados_filtrados.json'.")
