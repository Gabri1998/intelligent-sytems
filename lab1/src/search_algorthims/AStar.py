import heapq
import time  
from typing import Dict, List
from Search import Search
from utilities.Node import Node
from utilities.State import State
from utilities.RouteData import RouteData
from datetime import timedelta
class AStar(Search):
    def __init__(self, json_file_path: str, heuristic):
        super().__init__(json_file_path)
        self.heuristic = heuristic  # Heuristic function
        self.generated_nodes = 0
        self.expanded_nodes = 0

    def search(self):
        """Performs the A* search algorithm."""
        # Start tracking execution time
        start_time = time.time()

       
        frontier = []
        start_node = Node(self.problem.initial_state)
        heapq.heappush(frontier, (self.f(start_node), start_node))
        cost_so_far = {self.problem.initial_state: 0}

        while frontier:
            f_cost, node = heapq.heappop(frontier)
            print(f"Exploring: {node.state}")
            self.expanded_nodes += 1  # Track expanded nodes

            if self.problem.is_goal(node.state):
                end_time = time.time()
                print("Goal found!")
                return node.path(), end_time - start_time

            for action, successor, cost in self.problem.get_successors(node.state, include_cost=True):
                new_cost = cost_so_far[node.state] + cost
                if successor not in cost_so_far or new_cost < cost_so_far[successor]:
                    cost_so_far[successor] = new_cost
                    priority = new_cost + self.heuristic(successor)
                    heapq.heappush(frontier, (priority, Node(successor, node, action, new_cost)))
                    self.generated_nodes += 1  # Track generated nodes
                    print(f"Adding to frontier: {successor}")
        end_time = time.time()
        print("No solution found.")
        return None, end_time - start_time

    def f(self, node):
        """f(n) = g(n) + h(n): Path cost + heuristic."""
        return node.path_cost + self.heuristic(node.state)

    def write_solution_to_file(self, solution, execution_time, file_path):
        """Write the solution path and additional information to a text file."""
        with open(file_path, 'w') as f:
            if solution:
                f.write(f"Generated nodes: {self.generated_nodes}\n")
                f.write(f"Expanded nodes: {self.expanded_nodes}\n")
                f.write(f"Execution time: {execution_time}\n")
                f.write(f"Solution length: {len(solution) - 1}\n")
                solution_cost = solution[-1].path_cost
                formatted_cost = str(timedelta(seconds=solution_cost))
                f.write(f"Solution cost: {formatted_cost}\n")
                f.write("Solution Path:\n")
                
                for i, node in enumerate(solution):
                    f.write(f"{i + 1}: State ID {node.state.id} (lat: {node.state.latitude}, lon: {node.state.longitude})\n")
            else:
                f.write("No solution found.\n")

if __name__ == "__main__":
    def manhattan_heuristic(state, goal_state):
        """Manhattan distance heuristic for grid-based problems, handling missing values."""
        if state.latitude is None or state.longitude is None or goal_state.latitude is None or goal_state.longitude is None:
            return float('inf')  # High cost if coordinates are missing
        
        return abs(state.latitude - goal_state.latitude) + abs(state.longitude - goal_state.longitude)

    json_file_path = '/home/gabri/Inteilligent Systems/src/input/problems/huge/calle_cardenal_tabera_y_araoz_albacete_2000_1.json'
    astar = AStar(json_file_path, lambda state: manhattan_heuristic(state, astar.problem.goal_state))
    solution, execution_time = astar.search()

    if solution:
        astar.write_solution_to_file(solution, execution_time, '/home/gabri/Inteilligent Systems/src/output/huge/astar/plaza_isabel_ii_albacete_250_0.txt')
    else:
        print("No solution found.")
