from typing import List, Tuple
import random
from multiprocessing import Pool
from concurrent.futures import ProcessPoolExecutor

class GeneticAlgorithm:
    def __init__(self, problem, population_size=200, generations=50, mutation_rate=0.2, crossover_rate=0.8, tournament_size=3, penalty_time=None):
        self.problem = problem
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.tournament_size = tournament_size
        self.penalty_time = penalty_time

    def initialize_population(self) -> List[List[int]]:
        return [self.problem.generate_random_chromosome() for _ in range(self.population_size)]

    def evaluate_population(self, population: List[List[int]]) -> List[Tuple[List[int], float]]:
        return [(chromosome, self.problem.evaluate_solution(chromosome)) for chromosome in population]

    def select_parents(self, evaluated_population: List[Tuple[List[int], float]]) -> Tuple[List[int], List[int]]:
        """
        Select two parents using a tournament selection method.
        """
        tournament = random.sample(evaluated_population, self.tournament_size)
        tournament.sort(key=lambda x: x[1])
        return tournament[0][0], tournament[1][0]

    def crossover(self, parent1: List[int], parent2: List[int]) -> Tuple[List[int], List[int]]:
        """
        Perform one-point crossover and ensure children are valid.
        """
        if random.random() < self.crossover_rate:
            point = random.randint(1, len(parent1) - 1)
            child1 = parent1[:point] + parent2[point:]
            child2 = parent2[:point] + parent1[point:]
            return self.problem.fix_chromosome(child1), self.problem.fix_chromosome(child2)
        return parent1, parent2

    def mutate(self, chromosome: List[int]) -> List[int]:
        """
        Perform mutation by swapping two genes.
        """
        if random.random() < self.mutation_rate:
            idx1, idx2 = random.sample(range(len(chromosome)), 2)
            chromosome[idx1], chromosome[idx2] = chromosome[idx2], chromosome[idx1]
        return chromosome

    def search(self) -> Tuple[List[int], float]:
        """
        Perform the genetic algorithm search and return the best solution and its fitness.
        """
        population = self.initialize_population()
        best_solution = None
        best_fitness = float('inf')

        for generation in range(self.generations):
            evaluated_population = self.evaluate_population(population)
            evaluated_population.sort(key=lambda x: x[1])

            if evaluated_population[0][1] < best_fitness:
                best_solution, best_fitness = evaluated_population[0]

            new_population = []
            while len(new_population) < self.population_size:
                parent1, parent2 = self.select_parents(evaluated_population)
                child1, child2 = self.crossover(parent1, parent2)
                new_population.append(self.mutate(child1))
                if len(new_population) < self.population_size:
                    new_population.append(self.mutate(child2))

            # Combine old and new populations and keep the best individuals
            evaluated_new_population = self.evaluate_population(new_population)
            combined_population = evaluated_population + evaluated_new_population
            combined_population.sort(key=lambda x: x[1])
            population = [individual[0] for individual in combined_population[:self.population_size]]

        return best_solution, best_fitness
