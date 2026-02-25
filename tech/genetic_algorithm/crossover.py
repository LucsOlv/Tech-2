import random
from typing import List, Tuple

def order_crossover(parent1: List[Tuple[float, float]], parent2: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    """
    Realiza o cruzamento ordenado (OX - Order Crossover) entre duas sequências pai para criar uma sequência filha.

    Parâmetros:
    - parent1 (List[Tuple[float, float]]): A primeira sequência pai.
    - parent2 (List[Tuple[float, float]]): A segunda sequência pai.

    Retornos:
    List[Tuple[float, float]]: A sequência filha resultante do cruzamento ordenado.
    """
    length = len(parent1)

    # Escolhe dois índices aleatórios para o cruzamento
    start_index = random.randint(0, length - 1)
    end_index = random.randint(start_index + 1, length)

    # Inicializa o filho com uma cópia da substring correspondente ao parent1
    child = parent1[start_index:end_index]

    # Preenche as posições restantes com os genes do parent2
    remaining_positions = [i for i in range(length) if i < start_index or i >= end_index]
    remaining_genes = [gene for gene in parent2 if gene not in child]

    for position, gene in zip(remaining_positions, remaining_genes):
        child.insert(position, gene)

    return child
