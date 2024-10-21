from typing import Dict, List, Tuple
from State import State

class Problem:
    def __init__(self, initial_state: State, goal_state: State, graph: Dict = None):
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.graph = graph if graph is not None else {}

    def get_successors(self, state: State) -> List[Tuple[str, State]]:
        """Returns the possible actions, resulting states, and costs."""
        if state.id in self.graph:
            # Unpack action, next_state_id, and distance (though you may not need to use the distance here)
            return [(action, State(next_state_id, None, None)) for action, next_state_id, distance in self.graph[state.id]]
        return []

    def step_cost(self, current_state: State, action: str, next_state: State) -> float:
        """Return the actual cost (distance) between current_state and next_state."""
        for segment in self.graph[current_state.id]:
            if segment[1] == next_state.id:
                return segment[2]  # The distance (cost) is now the third element
        return 1  # Default cost if not found


    def is_goal(self, state: State) -> bool:
        """Checks if the given state is the goal state."""
        result = state == self.goal_state
        print(f"Checking if {state} is goal: {result}")
        return result

    def get_action_and_cost(self, state: State, next_state: State) -> Tuple[str, float]:
        """Retrieve the action and cost between two states."""
        for action, next_state_id, distance in self.graph[state.id]:
            if next_state_id == next_state.id:
                return action, distance  # Return the correct action and distance
        return "move", 1  # Default action and cost if not found