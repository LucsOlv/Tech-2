import networkx as nx
import osmnx as ox

def calculate_route_metrics(G, veiculos_rotas):
    """
    Calcula a distância total e o tempo total estimado para todas as rotas da frota.
    
    Args:
        G: Grafo OSMnx da cidade com velocidades e tempos de viagem nas arestas (add_edge_travel_times).
        veiculos_rotas: Matriz de rotas separada por veículos contendo tuplas de coordenadas (lat, lon).
        
    Returns:
        dict: Contém a 'total_distance_km' e 'total_time_minutes' da operação inteira.
    """
    if G is None or not veiculos_rotas:
        return {"total_distance_km": 0, "total_time_minutes": 0}

    total_meters = 0.0
    total_seconds = 0.0

    for sub_rota in veiculos_rotas:
        for i in range(len(sub_rota) - 1):
            p1 = sub_rota[i]
            p2 = sub_rota[i+1]
            
            try:
                # Encontra o nó mais próximo no grafo para as coordenadas de origem e destino
                orig_node = ox.distance.nearest_nodes(G, X=p1[1], Y=p1[0])
                dest_node = ox.distance.nearest_nodes(G, X=p2[1], Y=p2[0])
                
                # Pega a rota física no grafo calculada por menor tempo
                route_nodes = nx.shortest_path(G, orig_node, dest_node, weight="travel_time")
                
                # Itera sobre as arestas desse menor caminho para somar suas propriedades físicas reais
                for u, v in zip(route_nodes[:-1], route_nodes[1:]):
                    # Como OSMnx usa Multidigraph, pegamos os dados da aresta [0]
                    edge_data = G.get_edge_data(u, v)[0]
                    total_meters += edge_data.get("length", 0)
                    total_seconds += edge_data.get("travel_time", 0)
            except Exception as e:
                # Loga falhas; a aresta com problema simplesmente não contribui para os totais
                print(f"[metrics] Falha ao calcular métrica {p1} → {p2}: {e}")

    total_distance_km = total_meters / 1000.0
    total_time_minutes = total_seconds / 60.0

    return {
        "total_distance_km": round(total_distance_km, 2),
        "total_time_minutes": round(total_time_minutes, 2)
    }

def format_time(minutes):
    """Auxiliar para transformar minutos quebrados em string (ex: 1h 20m)"""
    if minutes < 60:
        return f"{int(minutes)}m"
    hours = int(minutes // 60)
    mins = int(minutes % 60)
    return f"{hours}h {mins}m"
