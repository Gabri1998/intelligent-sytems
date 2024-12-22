import random
from typing import List, Tuple

class RandomSearch:
    def __init__(self, problem, num_iterations=1000):
        """
        Initialize the Random Search.

        Args:
            problem: The Problem instance.
            num_iterations: Number of iterations to perform.
        """
        self.problem = problem
        self.num_iterations = num_iterations
        self.best_solution = None
        self.best_fitness = float('inf')

    def search(self) -> Tuple[List[int], float]:
        """
        Perform the Random Search.

        Returns:
            Tuple[List[int], float]: Best solution and its fitness score.
        """
        for _ in range(self.num_iterations):
            chromosome = self.problem.generate_random_chromosome()
            fitness = self.problem.evaluate_solution(chromosome)

            if fitness < self.best_fitness:
                self.best_solution = chromosome
                self.best_fitness = fitness

        return self.best_solution, self.best_fitness
