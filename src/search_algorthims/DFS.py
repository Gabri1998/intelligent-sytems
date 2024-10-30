import time 
from Search import Search
from utilities.Node import Node  # Import the Node class from the utilities folder


class DFS(Search):
    def __init__(self, json_file_path: str):
        super().__init__(json_file_path)
        self.generated_nodes = 0
        self.expanded_nodes = 0
        self.execution_time = 0
        self.solution_cost = 0

    def search(self):
        """Perform the DFS search."""
        start_time = time.time()  # Start tracking time
        frontier = [Node(self.problem.initial_state)]  # Use a stack for DFS
        self.checked = set()  # Track explored nodes

        while frontier:
            node = frontier.pop()  # DFS uses LIFO, pop from the end of the stack
            print(f"Exploring: {node.state}")
            self.expanded_nodes += 1  # Increment expanded nodes count

            if self.problem.is_goal(node.state):
                end_time = time.time()  # Stop tracking time
                self.execution_time = end_time - start_time  # Calculate execution time
                self.solution_cost = node.path_cost  # Total solution cost
                print("Goal found!")
                return node.path()  # Return the path to the goal

            self.checked.add(node.state)  # Mark the node as explored

            # Expand the node and add its children to the frontier
            for child in node.expand(self.problem):
                if child.state not in self.checked and child not in frontier:
                    frontier.append(child)
                    self.generated_nodes += 1  # Increment generated nodes count
                    print(f"Adding to frontier: {child.state}")

        end_time = time.time()  # Stop tracking time
        self.execution_time = end_time - start_time  # Calculate execution time
        print("No solution found after exploring all states.")
        return None

   
    def write_solution_to_file(self, solution, file_path):
        """Write solution path and info to file."""
        with open(file_path, 'w') as f:
            if solution:
                f.write(f"Generated nodes: {self.generated_nodes}\n")
                f.write(f"Expanded nodes: {self.expanded_nodes}\n")
                f.write(f"Solution length: {len(solution) - 1}\n")
                f.write("Solution: [")
                
                for i in range(len(solution) - 1):
                    current_node = solution[i]
                    next_node = solution[i + 1]
                    action = f"move to {next_node.state.id}"
                    cost = self.problem.step_cost(current_node.state, action, next_node.state)
                    f.write(f"{current_node.state.id} → {next_node.state.id}, cost: {cost}")
                    if i < len(solution) - 2:
                        f.write(", ")
                f.write("]\n")
            else:
                f.write("No solution found.\n")



if __name__ == "__main__":
    json_file_path = '/home/gabri/Inteilligent Systems/src/input/problems/small/plaza_isabel_ii_albacete_250_0.json'
    dfs = DFS(json_file_path)
    solution = dfs.search()  # Call the search method

    if solution:
        dfs.write_solution_to_file(solution,
                                   '/home/gabri/Inteilligent Systems/src/output/small/dfs/plaza_isabel_ii_albacete_250_0.txt')  # Write solution to file
    else:
        print("No solution found.")
