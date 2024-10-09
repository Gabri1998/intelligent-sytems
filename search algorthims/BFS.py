from collections import deque
from search_algorthims.Search import Search
from utilities.Node import Node  # Import the Node class from the utilities folder
from utilities.Problem import Problem  # Import the Problem class if needed
from utilities.State import State  # Import the State class if needed
from utilities.Action import Action  # Import the Action class if needed


class BFS(Search):
    def search(self):
        frontier = deque([Node(self.problem.initial_state)])  # Use a queue for BFS
        self.checked = set()

        while frontier:
            node = frontier.popleft()
            if self.problem.goal_test(node.state):
                self.solution = node.path()
                return self.solution
            self.checked.add(node.state)

            for child in node.expand(self.problem):
                if child.state not in self.checked and child not in frontier:
                    frontier.append(child)
        return None