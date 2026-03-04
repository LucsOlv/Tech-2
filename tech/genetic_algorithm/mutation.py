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
        
        # Garante que haja pelo menos três cidades (Origem + 2 destinos) para realizar a troca
        if len(solution) < 3:
            return solution
    
        # Seleciona um índice aleatório (excluindo o índice 0 que é a origem, e o último) para a troca
        index = random.randint(1, len(solution) - 2)
        
        # Troca a cidade no índice selecionado com o próximo índice
        mutated_solution[index], mutated_solution[index + 1] = solution[index + 1], solution[index]   
        
    return mutated_solution
