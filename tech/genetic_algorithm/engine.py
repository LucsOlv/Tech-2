import random
from typing import List, Tuple

from .population import generate_random_population, sort_population
from .fitness import calculate_fitness
from .crossover import order_crossover
from .mutation import mutate


def run_genetic_algorithm(
    cities_locations: List[Tuple[float, float]],
    population_size: int = 100,
    n_generations: int = 100,
    mutation_probability: float = 0.3
) -> List[List[Tuple[float, float]]]:
    """
    Executa o Algoritmo Genético para resolver o PCV (Problema do Caixeiro Viajante).

    Parâmetros:
    - cities_locations (List[Tuple[float, float]]): As coordenadas das cidades.
    - population_size (int): O tamanho da população.
    - n_generations (int): O número de gerações a serem executadas.
    - mutation_probability (float): A probabilidade de mutação para cada indivíduo.

    Retornos:
    List[List[Tuple[float, float]]]: A melhor solução encontrada em cada geração.
    """
    # CRIA A POPULAÇÃO INICIAL
    population = generate_random_population(cities_locations, population_size)

    # Listas para armazenar as melhores soluções para plotagem/análise
    best_solutions = []
    
    for _ in range(n_generations):
        population_fitness = [calculate_fitness(individual) for individual in population]    
        population, _ = sort_population(population, population_fitness)
        
        best_solution = population[0]
        best_solutions.append(best_solution)    

        new_population = [population[0]]  # Mantém o melhor indivíduo: ELITISMO
        
        while len(new_population) < population_size:
            
            # SELEÇÃO
            parent1, parent2 = random.choices(population[:10], k=2)  # Seleciona pais dentre os 10 melhores indivíduos
            
            # CRUZAMENTO
            child1 = order_crossover(parent1, parent2)
            
            ## MUTAÇÃO
            child1 = mutate(child1, mutation_probability)
            
            new_population.append(child1)
            
        population = new_population
    
    return best_solutions
