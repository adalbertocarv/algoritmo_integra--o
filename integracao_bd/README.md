## Documentação do Projeto de Roteamento de Ônibus com Integração

### **Visão Geral**
Este projeto implementa um sistema de roteamento para encontrar o caminho mais eficiente entre duas paradas de ônibus, considerando a possibilidade de integração em diferentes linhas. O sistema utiliza algoritmos de grafos e a técnica de serialização para melhorar a performance. O projeto está dividido em módulos para facilitar a manutenção, expansão e reutilização.

### **Arquitetura do Projeto**
O projeto é organizado da seguinte maneira:

```plaintext
bus_route_project/
│
├── main.py             # Arquivo principal que executa o algoritmo e a lógica de busca de rotas
├── database.py         # Módulo responsável por carregar os dados do banco de dados SQLite
├── graph.py            # Módulo para construção do grafo de conexões
├── a_star.py           # Módulo que contém a implementação do algoritmo A* com integração
└── utils.py            # Módulo utilitário (funções auxiliares como serialização com pickle)
```

### **Descrição dos Módulos**

#### **1. `main.py`**
O arquivo `main.py` é o ponto de entrada do programa. Ele coordena a execução do projeto, carregando dados, construindo o grafo, e utilizando o algoritmo A* para encontrar o caminho mais eficiente entre duas paradas.

**Funcionalidades:**
- Carrega o grafo do arquivo serializado, se disponível.
- Caso contrário, carrega os dados do banco de dados e constrói o grafo.
- Mantém o programa rodando para responder a múltiplas consultas.
- Imprime o caminho encontrado, incluindo as paradas, linhas, e pontos de integração.

#### **2. `database.py`**
O módulo `database.py` é responsável por carregar os dados do banco de dados SQLite. Ele extrai as paradas e as linhas de ônibus associadas e as retorna para uso posterior na construção do grafo.

**Funcionalidades:**
- Conecta ao banco de dados SQLite.
- Extrai os dados de paradas e linhas.
- Retorna os dados em estruturas de fácil manipulação (listas e dicionários).

**Motivação:**
- Separar a lógica de acesso a dados da lógica de processamento, facilitando a manutenção e possíveis mudanças na fonte de dados.

#### **3. `graph.py`**
O módulo `graph.py` é responsável por construir o grafo de conexões entre as paradas de ônibus, baseando-se nos dados de paradas e linhas extraídos do banco de dados.

**Funcionalidades:**
- Recebe as paradas e as linhas associadas.
- Constrói um grafo onde os nós são paradas e as arestas representam as linhas que conectam essas paradas.

**Motivação:**
- Manter a construção do grafo separada da lógica principal, permitindo alterações no modelo de dados sem impactar o restante do código.

#### **4. `a_star.py`**
Este módulo contém a implementação do algoritmo A* para encontrar o caminho mais eficiente entre duas paradas, com suporte à integração entre diferentes linhas.

**Funcionalidades:**
- Implementa o algoritmo A* para busca de caminhos.
- Utiliza uma heurística simples baseada na diferença entre IDs de paradas para priorizar a busca.
- Retorna o caminho completo, incluindo as paradas, linhas, e pontos de integração.

**Motivação:**
- Usar o A* devido à sua eficiência em encontrar o caminho mais curto, especialmente em grafos onde uma boa heurística pode ser aplicada.

#### **5. `utils.py`**
O módulo `utils.py` contém funções auxiliares, como as de serialização e desserialização do grafo utilizando `pickle`.

**Funcionalidades:**
- Serializa o grafo para um arquivo em disco para carregamento rápido em execuções futuras.
- Carrega o grafo do arquivo, se disponível, evitando a reconstrução desnecessária.

**Motivação:**
- Melhorar a performance do sistema, evitando o carregamento e a construção do grafo toda vez que o programa é executado.
- Centralizar funções utilitárias em um módulo separado para facilitar a manutenção e a reutilização.

### **Processo de Execução**
1. **Carregamento do Grafo**: Ao iniciar o programa, ele tenta carregar o grafo previamente serializado a partir de um arquivo. Isso reduz o tempo de inicialização, já que evita a reconstrução do grafo.
  
2. **Construção do Grafo**: Se o grafo não for encontrado no arquivo, ele é construído a partir dos dados carregados do banco de dados. Após a construção, o grafo é salvo em disco para execuções futuras.

3. **Execução do Algoritmo A***: Após o carregamento ou construção do grafo, o programa fica em execução contínua, aguardando a entrada do usuário para encontrar e retornar o caminho mais eficiente entre as paradas especificadas.

4. **Impressão do Caminho**: O caminho encontrado pelo algoritmo é impresso, detalhando as paradas e as linhas utilizadas, bem como os pontos de integração, se houver.

### **Motivações para as Soluções Escolhidas**

#### **1. Arquitetura Modular**
- **Motivação**: A arquitetura modular facilita a manutenção, expansão e teste do sistema. Cada módulo tem uma responsabilidade clara e bem definida, o que permite fazer alterações em uma parte do sistema sem afetar as outras.

#### **2. Serialização com `pickle`**
- **Motivação**: A serialização com `pickle` foi escolhida para evitar a necessidade de reconstruir o grafo a cada execução do programa, o que pode ser um processo demorado. A serialização melhora significativamente o tempo de resposta ao iniciar o programa, carregando rapidamente o grafo a partir de um arquivo.

#### **3. Algoritmo A***
- **Motivação**: O algoritmo A* foi escolhido por ser um dos mais eficientes para a busca de caminhos em grafos, especialmente quando há uma boa heurística disponível. Ele é particularmente útil em contextos onde o desempenho é crítico e onde a busca por rotas mais curtas é uma prioridade.

#### **4. Uso de SQLite**
- **Motivação**: SQLite foi escolhido por ser uma solução de banco de dados leve e fácil de configurar, ideal para um projeto de porte pequeno a médio. Ele permite manipular dados estruturados sem a necessidade de configurar um servidor de banco de dados completo.

### **Possíveis Expansões Futuras**
- **Integração com Dados em Tempo Real**: Adicionar a capacidade de integrar dados em tempo real, como atrasos ou congestionamentos, para melhorar a precisão das rotas sugeridas.
- **Aprimoramento da Heurística**: Substituir a heurística baseada em IDs por uma que use coordenadas geográficas, como a fórmula de Haversine, para calcular a distância real entre paradas.
- **Interface de Usuário**: Desenvolver uma interface gráfica ou uma API REST para facilitar o uso do sistema por usuários finais ou outros sistemas.

### **Conclusão**
Este projeto fornece uma base sólida para um sistema de roteamento de ônibus com suporte a integrações entre linhas. A escolha de uma arquitetura modular, combinada com o uso de técnicas de otimização como a serialização do grafo, garante um desempenho eficiente e facilita futuras expansões e melhorias.