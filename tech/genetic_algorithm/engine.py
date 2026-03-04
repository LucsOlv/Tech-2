import random
from typing import List, Tuple

from .population import generate_random_population, sort_population
from .fitness import calculate_fitness
from .crossover import order_crossover
from .mutation import mutate


def _tournament_selection(population: List, k: int = 4) -> List:
    """
    Seleção por torneio: escolhe k indivíduos aleatórios da população e retorna o melhor.
    Mais robusto que selecionar apenas entre os top-10, evitando convergência prematura.
    """
    competitors = random.sample(population, min(k, len(population)))
    return min(competitors, key=calculate_fitness)


def run_genetic_algorithm(
    cities_locations: List[Tuple[float, float]],
    population_size: int = 100,
    n_generations: int = 100,
    mutation_probability: float = 0.3,
    callback=None
) -> List[List[Tuple[float, float]]]:
    """
    Executa o Algoritmo Genético para resolver o PCV (Problema do Caixeiro Viajante).

    Parâmetros:
    - cities_locations (List[Tuple[float, float]]): As coordenadas das cidades.
    - population_size (int): O tamanho da população.
    - n_generations (int): O número de gerações a serem executadas.
    - mutation_probability (float): A probabilidade de mutação para cada indivíduo.

    Retornos:
    Tuple:
      - best_solutions (List): A melhor rota de cada geração (para análise/convergência).
      - best_route_global: A melhor rota encontrada em TODAS as gerações (min fitness global).
    """
    # CRIA A POPULAÇÃO INICIAL
    population = generate_random_population(cities_locations, population_size)

    # Lista de melhores fitness por geração (para análise de convergência)
    best_solutions = []
    # Rastreia a melhor rota global de forma incremental — sem re-varrer toda a lista ao final
    best_route_global = None
    best_fitness_global = float('inf')
    
    for generation in range(n_generations):
        population_fitness = [calculate_fitness(individual) for individual in population]    
        population, sorted_fitness = sort_population(population, population_fitness)
        
        best_solution = population[0]
        best_fitness = sorted_fitness[0]
        best_solutions.append(best_fitness)  # armazena apenas o valor, não a rota inteira

        # Atualiza o melhor global de forma incremental
        if best_fitness < best_fitness_global:
            best_fitness_global = best_fitness
            best_route_global = list(best_solution)
        
        if callback:
            callback(generation, best_fitness, best_solution)

        new_population = [population[0]]  # Mantém o melhor indivíduo: ELITISMO
        
        while len(new_population) < population_size:
            
            # SELEÇÃO por torneio — evita convergência prematura causada por top-10 fixo
            parent1 = _tournament_selection(population)
            parent2 = _tournament_selection(population)
            
            # CRUZAMENTO — gera 2 filhos por par (troca os papéis dos pais)
            child1 = order_crossover(parent1, parent2)
            child2 = order_crossover(parent2, parent1)
            
            ## MUTAÇÃO
            child1 = mutate(child1, mutation_probability)
            child2 = mutate(child2, mutation_probability)
            
            new_population.append(child1)
            if len(new_population) < population_size:
                new_population.append(child2)
            
        population = new_population
    
    return best_solutions, best_route_global
