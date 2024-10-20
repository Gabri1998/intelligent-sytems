import os
import json
from abc import ABC, abstractmethod
from typing import Any, List, Dict, Tuple  
from Problem import Problem
from State import State

class RouteData:
    """Class to handle route data from JSON."""

    def __init__(self, json_string: str):
        self.data = json.loads(json_string)

    def get_address(self) -> str:
        return self.data.get("address", "No Address")

    def get_distance(self) -> int:
        return self.data.get("distance", 0)

    def get_initial_final(self) -> Dict[str, int]:
        return {"initial": self.data.get("initial", 0), "final": self.data.get("final", 0)}

    def get_intersections(self) -> List[Dict[str, Any]]:
        return self.data.get("intersections", [])

    def get_segments(self) -> List[Dict[str, Any]]:
        return self.data.get("segments", [])


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
            graph[origin].append((f"move to {destination}", destination, distance))  # Include distance
            
            if destination not in graph:
                graph[destination] = []
            graph[destination].append((f"move to {origin}", origin, distance))  # Include distance
        
        return graph


    @abstractmethod
    def search(self):
        """Abstract method to perform the search."""
        pass

    def is_explored(self, state):
        """Check if a state has been checked."""
        return state in self.checked
