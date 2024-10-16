class Problem:
    def __init__(self, initial_state, goal_state):
        self.initial_state = initial_state
        self.goal_state = goal_state

    def goal_test(self, state):
        """Check if the state is the goal."""
        return state == self.goal_state

    def successor(self, state):
        """Return a list of (action, next_state) pairs representing possible transitions."""
        raise NotImplementedError("Define this based on the specific problem.")

    def step_cost(self, current_state, action, next_state):
        """Returns the cost of an action."""
        return action.cost
