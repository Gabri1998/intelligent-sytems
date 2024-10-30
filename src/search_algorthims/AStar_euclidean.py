import heapq
import math
import time
from Search import Search
from utilities.Node import Node
from utilities.State import State

class GreedyBestEuclidean(Search):
    def __init__(self, json_file_path: str):
        # Call the Search superclass to initialize the problem
        super().__init__(json_file_path)

    def search(self):
        # Track start time for execution duration
        start_time = time.time()

        frontier = []
        start_node = Node(self.problem.initial_state)
        
        # Calculate the Euclidean distance from start node to goal
        heapq.heappush(frontier, (self.euclidean_heuristic(start_node.state), start_node))
        
        self.generated_nodes = 0
        self.expanded_nodes = 0

        while frontier:
            _, current_node = heapq.heappop(frontier)
            self.expanded_nodes += 1

            print(f"Exploring: {current_node.state}")

            # Goal check
            if self.problem.is_goal(current_node.state):
                print("Goal found!")
                end_time = time.time()
                execution_time = end_time - start_time
                return current_node.path(), execution_time

            # Expand node to add successors
            for action, successor in self.problem.get_successors(current_node.state):
                if successor not in self.checked:
                    self.checked.add(successor)
                    priority = self.euclidean_heuristic(successor)
                    heapq.heappush(frontier, (priority, Node(successor, current_node, action)))
                    self.generated_nodes += 1
                    print(f"Adding to frontier: {successor}")

        print("No solution found.")
        return None, 0

    def euclidean_heuristic(self, state: State) -> float:
        """Calculate the Euclidean distance from a given state to the goal state."""
        goal = self.problem.goal_state
        if state.latitude is None or state.longitude is None or goal.latitude is None or goal.longitude is None:
            return float('inf')  # High cost if coordinates are missing
        return math.sqrt((state.latitude - goal.latitude) ** 2 + (state.longitude - goal.longitude) ** 2)

    def write_solution_to_file(self, solution, execution_time, file_path):
        """Write solution path and search metrics to a file."""
        with open(file_path, 'w') as f:
            if solution:
                f.write(f"Generated nodes: {self.generated_nodes}\n")
                f.write(f"Expanded nodes: {self.expanded_nodes}\n")
                f.write(f"Execution time: {execution_time:.6f}\n")
                f.write(f"Solution length: {len(solution) - 1}\n")
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

# Example usage
if __name__ == "__main__":
    json_file_path = '/home/gabri/Inteilligent Systems/src/input/problems/small/plaza_isabel_ii_albacete_250_0.json'
    greedy_search = GreedyBestEuclidean(json_file_path)
    solution, execution_time = greedy_search.search()
    
    if solution:
        output_path = '/home/gabri/Inteilligent Systems/src/output/small/gbs/plaza_isabel_ii_albacete_250_0.txt'
        greedy_search.write_solution_to_file(solution, execution_time, output_path)
    else:
        print("No solution found.")

