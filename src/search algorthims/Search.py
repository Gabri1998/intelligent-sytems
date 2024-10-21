import json
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple
from utilities.Problem import Problem
from utilities.State import State
from utilities.RouteData import RouteData

class Search(ABC):
    def __init__(self, json_file_path: str):
        self.route_data = self.load_route_data(json_file_path)
        self.problem = self.create_problem(self.route_data)
        self.solution = None
        self.checked = set()  # Keep track of checked states

    def load_route_data(self, file_path: str) -> RouteData:
        """Load the route data from a JSON file and return a RouteData instance."""
        with open(file_path, 'r') as f:
            json_string = f.read()
        return RouteData(json_string)

    def create_problem(self, route_data: RouteData):
        """Create a Problem instance from RouteData."""
        initial_state = State(route_data.get_initial_final()['initial'], None, None)
        goal_state = State(route_data.get_initial_final()['final'], None, None)
        graph = self.build_graph(route_data)  # Build the graph from route data
        return Problem(initial_state, goal_state, graph)

    def build_graph(self, route_data: RouteData) -> Dict[int, List[Tuple[str, int, float]]]:
        """Builds the graph using the segments from RouteData."""
        graph = {}
        for segment in route_data.get_segments():
            origin = segment["origin"]
            destination = segment["destination"]
            distance = segment["distance"]
            
            # Add bidirectional segments (or modify if directionality matters)
            if origin not in graph:
                graph[origin] = []
            graph[origin].append((f"move to {destination}", destination, distance))
            
            if destination not in graph:
                graph[destination] = []
            graph[destination].append((f"move to {origin}", origin, distance))
        
        return graph

    @abstractmethod
    def search(self):
        """Abstract method to perform the search."""
        pass

    def is_explored(self, state):
        """Check if a state has been checked."""
        return state in self.checked
