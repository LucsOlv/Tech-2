import requests
import polyline

def get_osrm_route(start_coords, end_coords):
    """
    Busca a rota entre duas coordenadas usando a API pública do OSRM.
    
    Args:
        start_coords (tuple): (latitude, longitude) de origem
        end_coords (tuple): (latitude, longitude) de destino
        
    Returns:
        list: Uma lista de coordenadas [(lat, lon), (lat, lon), ...] descrevendo a geometria da rota
              ou lista vazia em caso de falha.
    """
    # OSRM expects coordinates in (longitude, latitude) order
    start_lon, start_lat = start_coords[1], start_coords[0]
    end_lon, end_lat = end_coords[1], end_coords[0]
    
    osrm_url = f"http://router.project-osrm.org/route/v1/driving/{start_lon},{start_lat};{end_lon},{end_lat}?overview=full"
    
    try:
        response = requests.get(osrm_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data['code'] == 'Ok' and len(data['routes']) > 0:
                # Extrai a string de geometria codificada (Polyline) e decodifica para lat/lon
                encoded_polyline = data['routes'][0]['geometry']
                decoded_route = polyline.decode(encoded_polyline)
                return decoded_route
    except Exception as e:
        print(f"Erro ao buscar rota no OSRM: {e}")
        
    return []
