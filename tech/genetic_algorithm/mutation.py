import copy
import random
from typing import List, Tuple

def mutate(solution: List[Tuple[float, float]], mutation_probability: float) -> List[Tuple[float, float]]:
    """
    Muta uma solução invertendo um segmento da sequência com uma dada probabilidade de mutação.

    Parâmetros:
    - solution (List[Tuple[float, float]]): A sequência da solução a ser mutada.
    - mutation_probability (float): A probabilidade de mutação para cada indivíduo na solução.

    Retornos:
    List[Tuple[float, float]]: A sequência da solução mutada.
    """
    mutated_solution = copy.deepcopy(solution)

    # Verifica se a mutação deve ocorrer    
    if random.random() < mutation_probability:
        
        # Garante que haja pelo menos duas cidades para realizar a troca
        if len(solution) < 2:
            return solution
    
        # Seleciona um índice aleatório (excluindo o último índice) para a troca
        index = random.randint(0, len(solution) - 2)
        
        # Troca as cidades no índice selecionado e no próximo índice
        mutated_solution[index], mutated_solution[index + 1] = solution[index + 1], solution[index]   
        
    return mutated_solution
