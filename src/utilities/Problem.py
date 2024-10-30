from typing import Dict, List, Tuple
from utilities.State import State
from utilities.RouteData import RouteData


class Problem:
    def __init__(self, initial_state: State, goal_state: State, route_data: RouteData):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.route_data = route_data

   
    def get_action_and_cost(self, state1: State, state2: State) -> Tuple[str, float]:
        """Returns the action and cost between two states if a direct path exists."""
        for segment in self.route_data.get_segments(state1.id):  # Pass state1.id as the argument
            if segment["origin"] == state1.id and segment["destination"] == state2.id:
                action = f"move to {state2.id}"
                cost = segment["distance"]
                return action, cost
        return "", float('inf')  
 

   
    def get_successors(self, state, include_cost=False):
        """Return successors in the form of (action, successor_state, cost)"""
        successors = []
        for segment in self.route_data.get_segments(state.id):
            successor = self.route_data.get_state(segment['destination'])
            distance = segment['distance']
            speed = segment['speed']  # Assuming speed is given in meters per second
            
            # Convert distance to travel time
            travel_time = distance / speed  # cost as time in seconds

            action = f"move to {successor.id}"
            if include_cost:
                successors.append((action, successor, travel_time))  # Using travel time
            else:
                successors.append((action, successor))
        return successors

    def step_cost(self, current_state: State, action: str, next_state: State) -> float:
        """Retrieve the actual distance for step cost from JSON data."""
        for segment in self.route_data.get_segments(current_state.id):
            if segment["origin"] == current_state.id and segment["destination"] == next_state.id:
                return segment["distance"]
        return float('inf')  

    def is_goal(self, state: State) -> bool:
        return state.id == self.goal_state.id
