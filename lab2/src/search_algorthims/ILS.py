import random
from typing import List, Tuple
from search_algorthims.HC import HillClimbing

class IteratedLocalSearch:
    def __init__(self, problem, max_iterations: int = 1000, perturbation_strength: int = 2):
        """
        Initialize the Iterated Local Search (ILS) algorithm.

        Args:
            problem: The Problem instance with the configuration and evaluation logic.
            max_iterations (int): The maximum number of iterations to run.
            perturbation_strength (int): The number of bits to flip for perturbation.
        """
        self.problem = problem
        self.max_iterations = max_iterations
        self.perturbation_strength = perturbation_strength

    def perturb(self, chromosome: List[int]) -> List[int]:
        """
        Perturb the given chromosome by flipping a number of bits.

        Args:
            chromosome (List[int]): The chromosome to perturb.

        Returns:
            List[int]: A new perturbed chromosome.
        """
        perturbed = chromosome.copy()
        indices = random.sample(range(len(perturbed)), self.perturbation_strength)
        for idx in indices:
            perturbed[idx] = 1 - perturbed[idx]  # Flip the bit
        return self.problem.fix_chromosome(perturbed)

    def search(self) -> Tuple[List[int], float]:
        """
        Perform Iterated Local Search (ILS) to find the best solution for the problem.

        Returns:
            Tuple[List[int], float]: The best chromosome and its fitness score.
        """
        # Start with a random solution
        current = self.problem.generate_random_chromosome()
        current_fitness = self.problem.evaluate_solution(current)
        best_solution = current
        best_fitness = current_fitness

        for _ in range(self.max_iterations):
            # Apply local search (e.g., Hill Climbing)
            hc = HillClimbing(self.problem)
            current, current_fitness = hc.search()

            # If the new solution is better, update the best solution
            if current_fitness < best_fitness:
                best_solution = current
                best_fitness = current_fitness

            # Perturb the current solution to escape local minima
            current = self.perturb(best_solution)

        return best_solution, best_fitness
