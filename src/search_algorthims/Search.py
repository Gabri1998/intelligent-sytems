import json
from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple
from utilities.Problem import Problem
from utilities.State import State
from utilities.RouteData import RouteData

# Abstract base class for search algorithms
class Search(ABC):
    def __init__(self, json_file_path: str):
        """
        Initialize the Search class with essential data, including the route data,
        initial and goal states, and an instance of the Problem to be solved.
        """
        
        # Load route data from JSON file, which includes map details and intersections
        self.route_data = self.load_route_data(json_file_path)
        
        # Extract the initial and goal information from the route data
        initial_info = self.route_data.get_initial_final()
        intersections = {i["identifier"]: (i["latitude"], i["longitude"]) for i in self.route_data.get_intersections()}
        
        # Set up the initial and goal states using coordinates from intersections
        initial_coords = intersections.get(initial_info['initial'], (None, None))
        goal_coords = intersections.get(initial_info['final'], (None, None))
        
        initial_state = State(initial_info['initial'], *initial_coords)
        goal_state = State(initial_info['final'], *goal_coords)
        
        # Initialize the problem instance with initial and goal states and route data
        self.problem = Problem(initial_state, goal_state, self.route_data)
        
        # Initialize solution and checked nodes tracking
        self.solution = None
        self.checked = set()

    def load_route_data(self, file_path: str) -> RouteData:
        """
        Load route data from a JSON file, which provides the map data for the search problem.
        
        Args:
            file_path (str): Path to the JSON file containing route data.
            
        Returns:
            RouteData: An instance of RouteData populated with map details.
        """
        with open(file_path, 'r') as f:
            json_string = f.read()
        return RouteData(json_string)

    @abstractmethod
    def search(self):
        """
        Abstract method for executing the search algorithm. Each subclass implementing
        a specific search method (e.g., BFS, DFS, A*) must define this function.
        """
        pass

    def is_explored(self, state):
        """
        Check if a state has been previously checked (expanded).
        
        Args:
            state (State): The state to check.
            
        Returns:
            bool: True if the state is in the checked set, False otherwise.
        """
        return state in self.checked
