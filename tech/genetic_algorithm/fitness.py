import math
from typing import List, Tuple

def calculate_distance(point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
    """
    Calcula a distância Euclidiana entre dois pontos.

    Parâmetros:
    - point1 (Tuple[float, float]): As coordenadas do primeiro ponto.
    - point2 (Tuple[float, float]): As coordenadas do segundo ponto.

    Retornos:
    float: A distância Euclidiana entre os dois pontos.
    """
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def calculate_fitness(path: List[Tuple[float, float]]) -> float:
    """
    Calcula a aptidão de um caminho dado com base na distância Euclidiana total.

    Parâmetros:
    - path (List[Tuple[float, float]]): Uma lista de tuplas representando o caminho,
      onde cada tupla contém as coordenadas de um ponto.

    Retornos:
    float: A distância Euclidiana total do caminho.
    """
    distance = 0
    n = len(path)
    for i in range(n):
        distance += calculate_distance(path[i], path[(i + 1) % n])

    return distance
