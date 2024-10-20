class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0, depth=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = depth

    def expand(self, problem):
        """Returns child nodes from applying the problem's actions to this node."""
        return [
            Node(next_state,
                 parent=self,
                 action=action,
                 path_cost=self.path_cost + problem.step_cost(self.state, action, next_state))
            for action, next_state in problem.get_successors(self.state)  # Corrected to get_successors
        ]

    def path(self):
        """Returns the list of nodes from the root to this node."""
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    def __lt__(self, other):
        """Less than comparison for priority queue."""
        return self.path_cost < other.path_cost
