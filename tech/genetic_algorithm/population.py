import random
from typing import List, Tuple

def generate_random_population(cities_location: List[Tuple[float, float]], population_size: int) -> List[List[Tuple[float, float]]]:
    """
    Gera uma população aleatória de rotas para um determinado conjunto de cidades.

    Parâmetros:
    - cities_location (List[Tuple[float, float]]): Uma lista de tuplas representando as localizações das cidades,
      onde cada tupla contém a latitude e longitude.
    - population_size (int): O tamanho da população, ou seja, o número de rotas a serem geradas.

    Retornos:
    List[List[Tuple[float, float]]]: Uma lista de rotas, onde cada rota é representada como uma lista de localizações de cidades.
    """
    return [random.sample(cities_location, len(cities_location)) for _ in range(population_size)]


def sort_population(population: List[List[Tuple[float, float]]], fitness: List[float]) -> Tuple[List[List[Tuple[float, float]]], List[float]]:
    """
    Ordena uma população com base nos valores de aptidão (fitness).

    Parâmetros:
    - population (List[List[Tuple[float, float]]]): A população de soluções, onde cada solução é representada como uma lista.
    - fitness (List[float]): Os valores correspondentes de aptidão para cada solução na população.

    Retornos:
    Tuple[List[List[Tuple[float, float]]], List[float]]: Uma tupla contendo a população ordenada e os valores de aptidão ordenados correspondentes.
    """
    # Combina listas em pares
    combined_lists = list(zip(population, fitness))

    # Ordena com base nos valores da lista de aptidão
    sorted_combined_lists = sorted(combined_lists, key=lambda x: x[1])

    # Separa os pares ordenados de volta em listas individuais
    sorted_population, sorted_fitness = zip(*sorted_combined_lists)

    return list(sorted_population), list(sorted_fitness)
