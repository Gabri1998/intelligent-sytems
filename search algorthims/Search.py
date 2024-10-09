from abc import ABC, abstractmethod

class Search(ABC):
    def __init__(self, problem):
        self.problem = problem
        self.solution = None
        self.checked = set()  # Keep track of checked states

    @abstractmethod
    def search(self):
        """Abstract method to perform the search."""
        pass

    def is_explored(self, state):
        """Check if a state has been checked."""
        return state in self.checked
