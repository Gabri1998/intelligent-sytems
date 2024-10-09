import heapq
from search_algorthims.Search import Search
from utilities.Node import Node  # Import the Node class from the utilities folder
from utilities.Problem import Problem  # Import the Problem class if needed
from utilities.State import State  # Import the State class if needed
from utilities.Action import Action  # Import the Action class if needed


class UCS(Search):
    def search(self):
        frontier = []
        
        heapq.heappush(frontier, (0, Node(self.problem.initial_state)))  # Use a priority queue
        self.checked= set()

        while frontier:
            cost, node = heapq.heappop(frontier)
            if self.problem.goal_test(node.state):
                self.solution = node.path()
                return self.solution
            self.checked.add(node.state)

            for child in node.expand(self.problem):
                if child.state not in self.checked:
                    heapq.heappush(frontier, (child.path_cost, child))
        return None
