import time
from collections import deque
from Search import Search
from utilities.Node import Node
from datetime import timedelta
from decimal import Decimal, getcontext

# Set Decimal precision
getcontext().prec = 20

class BFS(Search):
    def __init__(self, json_file_path: str):
        super().__init__(json_file_path)
        self.generated_nodes = 0
        self.expanded_nodes = 0
        self.execution_time = 0
        self.solution_cost = 0

    def search(self):
        """Perform the BFS search with strict node tracking and clear separation of visited and queued nodes."""
        start_time = time.time()
        frontier = deque([Node(self.problem.initial_state)])
        visited = set()         # Nodes that have already been expanded
        queued = {self.problem.initial_state}  # Nodes that are currently in the frontier

        while frontier:
            node = frontier.popleft()
            self.expanded_nodes += 1
            print(f"Expanding: {node.state}")

            # Goal test after expansion
            if self.problem.is_goal(node.state):
                end_time = time.time()
                self.execution_time = end_time - start_time
                self.solution_cost = node.path_cost
                print("Goal found!")
                return node.path()

            visited.add(node.state)  # Mark this node as visited
            
            # Expand each child of the current node
            for child in node.expand(self.problem):
                if child.state not in visited and child.state not in queued:
                    frontier.append(child)
                    queued.add(child.state)  # Mark as queued to prevent re-queuing
                    self.generated_nodes += 1
                    print(f"Adding to frontier: {child.state}")

        end_time = time.time()
        self.execution_time = end_time - start_time
        print("No solution found after exploring all states.")
        return None

    def write_solution_to_file(self, solution, file_path):
        """Write the solution path and additional information to a text file."""
        with open(file_path, 'w') as f:
            if solution:
                f.write(f"Generated nodes: {self.generated_nodes}\n")
                f.write(f"Expanded nodes: {self.expanded_nodes}\n")
                
                # Format execution time to match the expected output format
                formatted_execution_time = str(timedelta(seconds=self.execution_time))
                f.write(f"Execution time: {formatted_execution_time}\n")
                
                f.write(f"Solution length: {len(solution) - 1}\n")
                
                # Format solution cost with exact precision
                solution_cost = solution[-1].path_cost
                formatted_cost = str(timedelta(seconds=solution_cost))
                f.write(f"Solution cost: {formatted_cost}\n")
                
                f.write("Solution: [")
                
                for i in range(len(solution) - 1):
                    current_node = solution[i]
                    next_node = solution[i + 1]
                    action, cost = self.problem.get_action_and_cost(current_node.state, next_node.state)
                    cost = Decimal(cost).quantize(Decimal('0.000000'))
                    f.write(f"{current_node.state.id} → {next_node.state.id} ({cost})")
                    if i < len(solution) - 2:
                        f.write(", ")
                f.write("]\n")
            else:
                f.write("No solution found.\n")


if __name__ == "__main__":
    json_file_path = '/home/gabri/Inteilligent Systems/src/input/problems/small/plaza_isabel_ii_albacete_250_0.json'
    bfs = BFS(json_file_path)
    solution = bfs.search()  # Call the search method

    if solution:
        output_path = '/home/gabri/Inteilligent Systems/src/output/small/bfs/plaza_isabel_ii_albacete_250_0.txt'
        bfs.write_solution_to_file(solution, output_path)  # Write solution to file
    else:
        print("No solution found.")
