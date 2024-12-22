import random
from typing import List, Tuple

class HillClimbing:
    def __init__(self, problem, max_iterations: int = 1000):
        """
        Initialize the Hill Climbing algorithm.
        
        Args:
            problem: The Problem instance with the configuration and evaluation logic.
            max_iterations (int): The maximum number of iterations to run.
        """
        self.problem = problem
        self.max_iterations = max_iterations

    def search(self) -> Tuple[List[int], float]:
        """
        Perform Hill Climbing to find the best solution for the problem.

        Returns:
            Tuple[List[int], float]: The best chromosome and its fitness score.
        """
        current = self.problem.generate_random_chromosome()
        current_fitness = self.problem.evaluate_solution(current)
        for _ in range(self.max_iterations):
            neighbor = current.copy()
            idx = random.randint(0, len(neighbor) - 1)
            neighbor[idx] = 1 - neighbor[idx]  # Flip a gene
            neighbor = self.problem.fix_chromosome(neighbor)
            neighbor_fitness = self.problem.evaluate_solution(neighbor)
            if neighbor_fitness < current_fitness:
                current = neighbor
                current_fitness = neighbor_fitness
        return current, current_fitness
