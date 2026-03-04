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
    # Protege a origem no índice 0
    if len(parent1) <= 1:
        return list(parent1)
        
    origin = parent1[0]
    p1_genes = parent1[1:]
    p2_genes = parent2[1:]
    
    length = len(p1_genes)

    # Escolhe dois índices aleatórios para o cruzamento no subconjunto de destinos
    start_index = random.randint(0, length - 1)
    end_index = random.randint(start_index + 1, length)

    # Inicializa o filho com None e copia o segmento de parent1
    child_genes = [None] * length
    child_genes[start_index:end_index] = p1_genes[start_index:end_index]

    # Preenche as posições restantes sequencialmente com os genes de parent2
    # que ainda não estão no filho (preserva ordem relativa do parent2)
    remaining_genes = [gene for gene in p2_genes if gene not in child_genes]
    remaining_iter = iter(remaining_genes)
    for i in range(length):
        if child_genes[i] is None:
            child_genes[i] = next(remaining_iter)

    # Reanexa a origem na posição inicial
    return [origin] + child_genes
