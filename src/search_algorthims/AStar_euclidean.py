import heapq
import math
import time
from Search import Search
from utilities.Node import Node
from utilities.State import State
from utilities.RouteData import RouteData

class AStarEuclidean(Search):
    def __init__(self, json_file_path: str):
        super().__init__(json_file_path)
        self.generated_nodes = 0
        self.expanded_nodes = 0

    def search(self):
        # Start tracking execution time
        start_time = time.time()
        
        frontier = []
        start_node = Node(self.problem.initial_state)
        heapq.heappush(frontier, (self.f(start_node), start_node))
        cost_so_far = {self.problem.initial_state: 0}

        while frontier:
            f_cost, node = heapq.heappop(frontier)
            print(f"Exploring: {node.state}")
            self.expanded_nodes += 1

            # Goal test
            if self.problem.is_goal(node.state):
                end_time = time.time()
                print("Goal found!")
                return node.path(), end_time - start_time

            # Expand the node
            for action, successor, cost in self.problem.get_successors(node.state, include_cost=True):
                # Using travel time as cost
                new_cost = cost_so_far[node.state] + cost  
                if successor not in cost_so_far or new_cost < cost_so_far[successor]:
                    cost_so_far[successor] = new_cost
                    priority = new_cost + self.euclidean_heuristic(successor)
                    heapq.heappush(frontier, (priority, Node(successor, node, action, new_cost)))
                    self.generated_nodes += 1
                    print(f"Adding to frontier: {successor}")

        end_time = time.time()
        return None, end_time - start_time

    def f(self, node):
        """f(n) = g(n) + h(n): Path cost plus heuristic estimate to goal."""
        return node.path_cost + self.euclidean_heuristic(node.state)

    def euclidean_heuristic(self, state: State) -> float:
        """Calculate the Euclidean distance heuristic, scaled to estimate travel time."""
        goal = self.problem.goal_state
        avg_speed = 30  # average speed in meters per second
        
        if state.latitude is None or state.longitude is None or goal.latitude is None or goal.longitude is None:
            return float('inf')

        # Euclidean distance to travel time
        distance = math.sqrt((state.latitude - goal.latitude) ** 2 + (state.longitude - goal.longitude) ** 2)
        estimated_time = distance / avg_speed
        return estimated_time

    def write_solution_to_file(self, solution, execution_time, file_path):
        """Write the solution path and additional information to a text file."""
        with open(file_path, 'w') as f:
            if solution:
                f.write(f"Generated nodes: {self.generated_nodes}\n")
                f.write(f"Expanded nodes: {self.expanded_nodes}\n")
                f.write(f"Execution time: {execution_time}\n")
                f.write(f"Solution length: {len(solution) - 1}\n")
                f.write(f"Solution cost: {solution[-1].path_cost}\n")
                f.write("Solution: [")
                
                for i in range(len(solution) - 1):
                    current_node = solution[i]
                    next_node = solution[i + 1]
                    action, cost = self.problem.get_action_and_cost(current_node.state, next_node.state)
                    f.write(f"{current_node.state.id} → {next_node.state.id}, {cost}")
                    if i < len(solution) - 2:
                        f.write(", ")
                f.write("]\n")
            else:
                f.write("No solution found.\n")


if __name__ == "__main__":
    json_file_path = '/home/gabri/Inteilligent Systems/src/input/problems/small/plaza_isabel_ii_albacete_250_0.json'
    astar = AStarEuclidean(json_file_path)
    solution, execution_time = astar.search()

    if solution:
        astar.write_solution_to_file(solution, execution_time, '/home/gabri/Inteilligent Systems/src/output/small/astar_euclidean/plaza_isabel_ii_albacete_250_0.txt')
    else:
        print("No solution found.")
