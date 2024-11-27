import time
from Search import Search
from utilities.Node import Node
from datetime import timedelta
from decimal import Decimal, getcontext

# Set Decimal precision for cost formatting
getcontext().prec = 20

# Depth-First Search (DFS) implementation with controlled traversal and output
class DFS(Search):
    def __init__(self, json_file_path: str):
        # Initialize the search by setting up problem data and tracking variables
        super().__init__(json_file_path)
        self.generated_nodes = 0  # Count nodes added to the frontier
        self.expanded_nodes = 0   # Count nodes that have been expanded
        self.execution_time = 0   # Track the time spent on the search
        self.solution_cost = 0    # Store the cost of the found solution path

    def search(self):
        """Perform DFS search without backtracking pruning and with node ordering for consistency."""
        
        # Start timing the execution
        start_time = time.time()
        
        # Initialize the frontier (stack for DFS) with the initial state
        frontier = [Node(self.problem.initial_state)]
        self.checked = set()  # Track expanded nodes to avoid revisiting

        while frontier:
            # Pop the last node from the stack (LIFO behavior for DFS)
            node = frontier.pop()
            
            # Skip nodes already expanded
            if node.state in self.checked:
                continue

            # Mark the current node as explored
            print(f"Exploring: {node.state}")
            self.checked.add(node.state)
            self.expanded_nodes += 1

            # Check if we've reached the goal state
            if self.problem.is_goal(node.state):
                # Calculate total execution time and solution cost
                self.execution_time = time.time() - start_time
                self.solution_cost = node.path_cost
                print("Goal found!")
                return node.path()  # Return the solution path

            # Expand the current node to generate successors
            successors = node.expand(self.problem)
            
            # Sort successors by state ID to ensure consistent traversal order
            successors.sort(key=lambda x: x.state.id)

            # Add each child to the frontier if it hasn't been expanded
            for child in successors:
                if child.state not in self.checked:
                    frontier.append(child)  # Add child to the stack
                    self.generated_nodes += 1  # Track the generated nodes
                    print(f"Adding to frontier: {child.state}")

        # If the stack is empty and no solution was found
        self.execution_time = time.time() - start_time
        print("No solution found after exploring all states.")
        return None

    def write_solution_to_file(self, solution, file_path):
        """Write solution details, including node statistics and path, to a file."""
        
        with open(file_path, 'w') as f:
            if solution:
                # Write statistics on generated and expanded nodes
                f.write(f"Generated nodes: {self.generated_nodes}\n")
                f.write(f"Expanded nodes: {self.expanded_nodes}\n")
                
                # Format execution time to match expected output
                formatted_execution_time = str(timedelta(seconds=self.execution_time))
                f.write(f"Execution time: {formatted_execution_time}\n")
                
                # Write the solution length (number of steps to reach goal)
                f.write(f"Solution length: {len(solution) - 1}\n")
                
                # Format and write the total cost of the solution path
                solution_cost = solution[-1].path_cost
                formatted_cost = str(timedelta(seconds=solution_cost))
                f.write(f"Solution cost: {formatted_cost}\n")
                
                # Write out the solution path, including actions and costs
                f.write("Solution: [")
                
                for i in range(len(solution) - 1):
                    current_node = solution[i]
                    next_node = solution[i + 1]
                    action, cost = self.problem.get_action_and_cost(current_node.state, next_node.state)
                    
                    # Format cost with six decimal precision
                    cost = Decimal(cost).quantize(Decimal('0.000000'))
                    f.write(f"{current_node.state.id} → {next_node.state.id} ({cost})")
                    if i < len(solution) - 2:
                        f.write(", ")
                f.write("]\n")
            else:
                # Indicate if no solution was found
                f.write("No solution found.\n")

# Main function to run DFS on a specific problem instance
if __name__ == "__main__":
    # Define path to the input JSON file
    json_file_path = '/home/gabri/Inteilligent Systems/src/input/problems/huge/calle_cardenal_tabera_y_araoz_albacete_2000_1.json'
    
    # Create a DFS instance and run the search
    dfs = DFS(json_file_path)
    solution = dfs.search()

    # Write the solution to a file if found, otherwise print "No solution found"
    if solution:
        output_path = '/home/gabri/Inteilligent Systems/src/output/huge/dfs/plaza_isabel_ii_albacete_250_0.txt'
        dfs.write_solution_to_file(solution, output_path)
    else:
        print("No solution found.")
