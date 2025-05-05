

class Action:
    def __init__(self, name, cost=1):
        """
        Initialize an action with a name and an associated cost.
        
        Args:
            name (str): The name or description of the action.
            cost (float): The cost of performing this action. Default is 1.
        """
        self.name = name
        self.cost = cost

    def __repr__(self):
        """String representation of the action, useful for debugging."""
        return f"Action({self.name}, cost={self.cost})"
