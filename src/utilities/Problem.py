from typing import Dict, List, Tuple
from utilities.State import State
from utilities.RouteData import RouteData

class Problem:
    def __init__(self, initial_state: State, goal_state: State, route_data: RouteData):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.route_data = route_data
        self.sorted_segments = self._sort_segments()  # Reintroduce sorted segments

    def _sort_segments(self) -> Dict[int, List[Dict]]:
        """Sort segments by destination to ensure predictable path traversal."""
        sorted_segments = {}
        for segment in self.route_data.segments:
            origin = segment["origin"]
            if origin not in sorted_segments:
                sorted_segments[origin] = []
            sorted_segments[origin].append(segment)

        for origin in sorted_segments:
            sorted_segments[origin].sort(key=lambda x: x["destination"])  # Sort by destination
        return sorted_segments

    def get_action_and_cost(self, state1: State, state2: State) -> Tuple[str, float]:
        """Returns the action and cost (scaled travel time) between two states if a direct path exists."""
        segments_from_state = self.sorted_segments.get(state1.id, [])
        for segment in segments_from_state:
            if segment["destination"] == state2.id:
                action = f"move to {state2.id}"
                travel_time = (segment["distance"] / segment["speed"]) * 3.6
                return action, travel_time
        return "", float('inf')  

    def get_successors(self, state: State, include_cost=False) -> List[Tuple[str, State, float]]:
        """Return successors, keeping sorted order."""
        successors = []
        segments_from_state = self.sorted_segments.get(state.id, [])

        for segment in segments_from_state:
            successor = self.route_data.get_state(segment['destination'])
            travel_time = (segment['distance'] / segment['speed']) * 3.6
            action = f"move to {successor.id}"
            if include_cost:
                successors.append((action, successor, travel_time))
            else:
                successors.append((action, successor))
        return successors

    def step_cost(self, current_state: State, action: str, next_state: State) -> float:
        segments_from_state = self.sorted_segments.get(current_state.id, [])
        for segment in segments_from_state:
            if segment["destination"] == next_state.id:
                return (segment["distance"] / segment["speed"]) * 3.6
        return float('inf')  

    def is_goal(self, state: State) -> bool:
        return state.id == self.goal_state.id
