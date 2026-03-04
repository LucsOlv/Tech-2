import osmnx as ox
import networkx as nx
import streamlit as st

@st.cache_resource(show_spinner="Baixando malha viária da cidade (ISSO PODE DEMORAR NA PRIMEIRA VEZ)...")
def get_city_graph(city_name):
    """
    Baixa e armazena em cache o grafo da malha viária (ruas) da cidade usando OSMnx.
    O cache mantem o grafo na memória para não baixar novamente enquanto o app estiver rodando.
    """
    try:
        # Baixa a malha dirigível (drive)
        G = ox.graph_from_place(city_name, network_type="drive", simplify=True)
        # Calcula as estimativas de velocidade e tempo de viagem nas arestas
        G = ox.add_edge_speeds(G)
        G = ox.add_edge_travel_times(G)
        return G
    except Exception as e:
        print(f"Erro ao baixar grafo da cidade {city_name}: {e}")
        return None

def get_osmnx_route(G, start_coords, end_coords):
    """
    Busca a rota mais curta entre duas coordenadas usando rede OSMnx via NetworkX.
    
    Args:
        G: Grafo NetworkX/OSMnx da cidade
        start_coords (tuple): (latitude, longitude) de origem
        end_coords (tuple): (latitude, longitude) de destino
        
    Returns:
        list: Uma lista de coordenadas [(lat, lon), (lat, lon), ...] descrevendo a geometria da rota
              ou lista vazia em caso de falha.
    """
    if G is None:
        return []

    try:
        # Encontra o nó mais próximo no grafo para as coordenadas de origem e destino
        orig_node = ox.distance.nearest_nodes(G, X=start_coords[1], Y=start_coords[0])
        dest_node = ox.distance.nearest_nodes(G, X=end_coords[1], Y=end_coords[0])
        
        # Calcula o caminho mais curto baseado no tempo de viagem (travel_time)
        try:
            route = nx.shortest_path(G, orig_node, dest_node, weight="travel_time")
        except nx.NetworkXNoPath:
            # Fallback para distância mais curta caso o tempo de viagem falhe em alguma rua
            route = nx.shortest_path(G, orig_node, dest_node, weight="length")
            
        # Converte os nós retornados nas coordenadas reais respectivas
        route_coords = []
        for node in route:
            lat = G.nodes[node]['y']
            lon = G.nodes[node]['x']
            route_coords.append((lat, lon))
            
        return route_coords
    except Exception as e:
        pass
        
    return []
