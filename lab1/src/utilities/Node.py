class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0, depth=0):
        """
        Initialize a node with state, parent, action, path cost, and depth information.
        
        Args:
            state (State): The current state of the node.
            parent (Node): The parent node from which this node was reached.
            action (Action): The action leading to this node.
            path_cost (float): The cumulative path cost to reach this node.
            depth (int): The depth of this node in the search tree.
        """
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = depth

    def expand(self, problem):
        """
        Generate child nodes for this node by applying actions to the current state.
        
        Args:
            problem (Problem): The problem defining state transitions and costs.
            
        Returns:
            List[Node]: A list of child nodes.
        """
        return [
            Node(next_state,
                 parent=self,
                 action=action,
                 path_cost=self.path_cost + problem.step_cost(self.state, action, next_state))
            for action, next_state in problem.get_successors(self.state)
        ]

    def path(self):
        """
        Trace back from the current node to the root to get the path.
        
        Returns:
            List[Node]: A list of nodes from the root to this node.
        """
        node, path_back = self, []
        while node:
            path_back.append(node)
            node = node.parent
        return list(reversed(path_back))

    def __lt__(self, other):
        """
        Compare nodes by path cost for priority queue handling.
        
        Args:
            other (Node): Another node to compare to.
            
        Returns:
            bool: True if this node's path cost is less than the other node's.
        """
        return self.path_cost < other.path_cost
