from typing import Dict, List, Tuple
from utilities.State import State
from utilities.RouteData import RouteData

class Problem:
    def __init__(self, initial_state: State, goal_state: State, route_data: RouteData):
        """
        Initialize the search problem with initial and goal states and route data.
        
        Args:
            initial_state (State): The starting state for the search.
            goal_state (State): The goal state for the search.
            route_data (RouteData): Data about routes, intersections, and segments.
        """
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.route_data = route_data
        self.sorted_segments = self._sort_segments()

    def _sort_segments(self) -> Dict[int, List[Dict]]:
        """
        Organize segments by origin state, sorted by destination for predictable traversal.
        
        Returns:
            Dict[int, List[Dict]]: A dictionary mapping state IDs to sorted segment lists.
        """
        sorted_segments = {}
        for segment in self.route_data.segments:
            origin = segment["origin"]
            if origin not in sorted_segments:
                sorted_segments[origin] = []
            sorted_segments[origin].append(segment)

        for origin in sorted_segments:
            sorted_segments[origin].sort(key=lambda x: x["destination"])
        return sorted_segments

    def get_action_and_cost(self, state1: State, state2: State) -> Tuple[str, float]:
        """
        Get the action and travel cost between two states if a direct path exists.
        
        Args:
            state1 (State): The starting state.
            state2 (State): The destination state.
            
        Returns:
            Tuple[str, float]: The action description and travel cost, or high cost if no path exists.
        """
        segments_from_state = self.sorted_segments.get(state1.id, [])
        for segment in segments_from_state:
            if segment["destination"] == state2.id:
                action = f"move to {state2.id}"
                travel_time = (segment["distance"] / segment["speed"]) * 3.6
                return action, travel_time
        return "", float('inf')  

    def get_successors(self, state: State, include_cost=False) -> List[Tuple[str, State, float]]:
        """
        Generate successor states for a given state.
        
        Args:
            state (State): The state to expand.
            include_cost (bool): Whether to include travel cost in the output.
            
        Returns:
            List[Tuple[str, State, float]]: List of tuples containing action, successor, and cost.
        """
        successors = []
        segments_from_state = self.sorted_segments.get(state.id, [])

        for segment in segments_from_state:
            successor = self.route_data.get_state(segment['destination'])
            travel_time = (segment["distance"] / segment["speed"]) * 3.6
            action = f"move to {successor.id}"
            if include_cost:
                successors.append((action, successor, travel_time))
            else:
                successors.append((action, successor))
        return successors

    def step_cost(self, current_state: State, action: str, next_state: State) -> float:
        """
        Get the cost between the current state and the next state if there's a direct segment.
        
        Args:
            current_state (State): The starting state.
            action (str): The action taken.
            next_state (State): The destination state.
            
        Returns:
            float: The travel cost between states, or high cost if no direct segment exists.
        """
        segments_from_state = self.sorted_segments.get(current_state.id, [])
        for segment in segments_from_state:
            if segment["destination"] == next_state.id:
                return (segment["distance"] / segment["speed"]) * 3.6
        return float('inf')  

    def is_goal(self, state: State) -> bool:
        """
        Check if a state is the goal state.
        
        Args:
            state (State): The state to check.
            
        Returns:
            bool: True if state is the goal state, False otherwise.
        """
        return state.id == self.goal_state.id
