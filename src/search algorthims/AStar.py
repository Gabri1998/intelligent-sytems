import heapq
from Search import Search
from utilities.Node import Node  # Import the Node class from the utilities folder
from utilities.Problem import Problem  # Import the Problem class if needed
from utilities.State import State  # Import the State class if needed
from utilities.Action import Action  # Import the Action class if needed



class AStar(Search):
    def __init__(self, problem, heuristic):
        super().__init__(problem)
        self.heuristic = heuristic  # Heuristic function h(n)

    def search(self):
        frontier = []
        start_node = Node(self.problem.initial_state)
        heapq.heappush(frontier, (self.f(start_node), start_node))  # Use a priority queue
        self.checked = set()

        while frontier:
            f_cost, node = heapq.heappop(frontier)
            if self.problem.goal_test(node.state):
                self.solution = node.path()
                return self.solution
            self.checked.add(node.state)

            for child in node.expand(self.problem):
                if child.state not in self.checked:
                    heapq.heappush(frontier, (self.f(child), child))
        return None

    def f(self, node):
        """f(n) = g(n) + h(n): Path cost plus heuristic estimate to goal."""
        return node.path_cost + self.heuristic(node.state)


    def manhattan_heuristic(state, goal_state):
        return abs(state.latitude - goal_state.latitude) + abs(state.longitude - goal_state.longitude)
