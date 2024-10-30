import json
from abc import ABC, abstractmethod
from typing import Any, List, Dict, Tuple  
from utilities.Problem import Problem
from utilities.State import State
from utilities.RouteData import RouteData

class Search(ABC):
    def __init__(self, json_file_path: str):
        self.route_data = self.load_route_data(json_file_path)
        initial_info = self.route_data.get_initial_final()
        intersections = {i["identifier"]: (i["latitude"], i["longitude"]) for i in self.route_data.get_intersections()}
        
        initial_coords = intersections.get(initial_info['initial'], (None, None))
        goal_coords = intersections.get(initial_info['final'], (None, None))
        
        initial_state = State(initial_info['initial'], *initial_coords)
        goal_state = State(initial_info['final'], *goal_coords)
        
        self.problem = Problem(initial_state, goal_state, self.route_data)
        self.solution = None
        self.checked = set()
        
    def load_route_data(self, file_path: str) -> RouteData:
        with open(file_path, 'r') as f:
            json_string = f.read()
        return RouteData(json_string)

    @abstractmethod
    def search(self):
        pass


    def is_explored(self, state):
        """Check if a state has been checked."""
        return state in self.checked
