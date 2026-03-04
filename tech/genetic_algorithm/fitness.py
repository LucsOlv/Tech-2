import math
from typing import List, Tuple

_EARTH_RADIUS_KM = 6371.0

def calculate_distance(point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
    """
    Calcula a distância Haversine entre dois pontos geográficos (lat, lon) em quilômetros.
    Substitui a distância Euclidiana para refletir distâncias reais na superfície da Terra,
    tornando o fitness do GA consistente com o roteamento real por ruas.

    Parâmetros:
    - point1 (Tuple[float, float]): (latitude, longitude) do primeiro ponto em graus.
    - point2 (Tuple[float, float]): (latitude, longitude) do segundo ponto em graus.

    Retornos:
    float: A distância em quilômetros entre os dois pontos.
    """
    lat1, lon1 = math.radians(point1[0]), math.radians(point1[1])
    lat2, lon2 = math.radians(point2[0]), math.radians(point2[1])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))

    return _EARTH_RADIUS_KM * c


def calculate_fitness(path: List[Tuple[float, float]]) -> float:
    """
    Calcula a aptidão de um caminho dado com base na distância Haversine total.

    Parâmetros:
    - path (List[Tuple[float, float]]): Uma lista de tuplas representando o caminho,
      onde cada tupla contém as coordenadas (latitude, longitude) de um ponto.

    Retornos:
    float: A distância Haversine total do caminho em quilômetros.
    """
    distance = 0
    n = len(path)
    for i in range(n):
        distance += calculate_distance(path[i], path[(i + 1) % n])

    return distance
