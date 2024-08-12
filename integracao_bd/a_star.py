import heapq
from collections import defaultdict
from utils import heuristic

def a_star_search(graph, origem, destino):
    open_set = []
    heapq.heappush(open_set, (0, origem))
    
    came_from = {}
    g_score = defaultdict(lambda: float('inf'))
    g_score[origem] = 0
    
    f_score = defaultdict(lambda: float('inf'))
    f_score[origem] = heuristic(origem, destino)
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current == destino:
            return reconstruct_path(came_from, current)
        
        for linha, neighbor in graph[current]:
            tentative_g_score = g_score[current] + 1  # Supondo um custo uniforme por parada
            
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = (current, linha)
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, destino)
                
                if neighbor not in open_set:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    return "No Path Found"

def reconstruct_path(came_from, current):
    total_path = []
    while current in came_from:
        current, linha = came_from[current]
        total_path.append((current, linha))
    return total_path[::-1]
