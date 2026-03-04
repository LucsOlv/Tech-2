import copy
import random
from typing import List, Tuple

def mutate(solution: List[Tuple[float, float]], mutation_probability: float) -> List[Tuple[float, float]]:
    """
    Muta uma solução usando o operador 2-opt: inverte um segmento aleatório da rota.
    É o operador de mutação padrão para TSP — gera muito mais diversidade do que
    a simples troca de vizinhos adjacentes e converge mais rápido para boas soluções.

    Parâmetros:
    - solution (List[Tuple[float, float]]): A sequência da solução a ser mutada.
    - mutation_probability (float): A probabilidade de mutação para cada indivíduo na solução.

    Retornos:
    List[Tuple[float, float]]: A sequência da solução mutada.
    """
    # Verifica se a mutação deve ocorrer
    if random.random() >= mutation_probability:
        return solution

    # Garante que haja pelo menos origem + 3 destinos para inverter um segmento não trivial
    if len(solution) < 4:
        return solution

    mutated_solution = copy.deepcopy(solution)

    # Seleciona dois índices distintos dentro dos destinos (excluindo índice 0 = origem)
    i = random.randint(1, len(solution) - 2)
    j = random.randint(i + 1, len(solution) - 1)

    # 2-opt: inverte o segmento entre i e j (inclusive)
    mutated_solution[i:j + 1] = reversed(mutated_solution[i:j + 1])

    return mutated_solution
