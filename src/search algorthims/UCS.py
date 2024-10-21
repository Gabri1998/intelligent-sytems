import heapq
from Search import Search
from Node import Node  # Import the Node class from the utilities folder
from Problem import Problem  # Import the Problem class if needed
from State import State  # Import the State class if needed
from Action import Action  # Import the Action class if needed


class UCS(Search):
    def __init__(self):
        self.search = Search()
    
    
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
