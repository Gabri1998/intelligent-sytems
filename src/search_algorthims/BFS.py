import time
from collections import deque
from Search import Search
from utilities.Node import Node
from datetime import timedelta
from decimal import Decimal, getcontext

# Set the precision for Decimal calculations (useful for cost formatting)
getcontext().prec = 20

# Breadth-First Search (BFS) implementation that uses strict node tracking with clear separation between visited and queued nodes.
class BFS(Search):
    def __init__(self, json_file_path: str):
        super().__init__(json_file_path)
        self.generated_nodes = 0  # Counts nodes added to the frontier
        self.expanded_nodes = 0   # Counts nodes that have been expanded
        self.execution_time = 0   # Tracks total execution time
        self.solution_cost = 0    # Total cost of the solution path if found

    def search(self):
        """Perform a BFS search with careful node tracking."""
        
        # Start measuring time for performance tracking
        start_time = time.time()
        
        # Initialize frontier as a queue and add the initial state as the starting point
        frontier = deque([Node(self.problem.initial_state)])
        
        # Track which nodes have been expanded or are currently in the frontier
        visited = set()  # Nodes that have already been expanded
        queued = {self.problem.initial_state}  # Nodes that are in the frontier to avoid re-adding

        while frontier:
            # Take the next node from the frontier (FIFO)
            node = frontier.popleft()
            self.expanded_nodes += 1  # Count each expansion
            print(f"Expanding: {node.state}")

            # Check if the current node is the goal
            if self.problem.is_goal(node.state):
                end_time = time.time()
                self.execution_time = end_time - start_time  # Total time taken to find the solution
                self.solution_cost = node.path_cost  # Total cost to reach the goal
                print("Goal found!")
                return node.path()  # Return the solution path

            # Mark the current node as visited after expansion
            visited.add(node.state)

            # Add each child of the current node to the frontier
            for child in node.expand(self.problem):
                # Only add child nodes that haven't been expanded or queued
                if child.state not in visited and child.state not in queued:
                    frontier.append(child)  # Add child node to frontier
                    queued.add(child.state)  # Mark it as queued
                    self.generated_nodes += 1  # Count generated nodes
                    print(f"Adding to frontier: {child.state}")

        # If the queue is empty and the goal wasn't found
        end_time = time.time()
        self.execution_time = end_time - start_time
        print("No solution found after exploring all states.")
        return None

    def write_solution_to_file(self, solution, file_path):
        """Write the solution path and various statistics to a file."""
        
        with open(file_path, 'w') as f:
            if solution:
                # Write node generation and expansion stats
                f.write(f"Generated nodes: {self.generated_nodes}\n")
                f.write(f"Expanded nodes: {self.expanded_nodes}\n")
                
                # Format and write execution time to match expected output format
                formatted_execution_time = str(timedelta(seconds=self.execution_time))
                f.write(f"Execution time: {formatted_execution_time}\n")
                
                # Write solution length (number of steps to reach goal)
                f.write(f"Solution length: {len(solution) - 1}\n")
                
                # Format and write the cost of the solution path
                solution_cost = solution[-1].path_cost
                formatted_cost = str(timedelta(seconds=solution_cost))
                f.write(f"Solution cost: {formatted_cost}\n")
                
                # Write the solution path, including actions and costs between states
                f.write("Solution: [")
                
                for i in range(len(solution) - 1):
                    current_node = solution[i]
                    next_node = solution[i + 1]
                    action, cost = self.problem.get_action_and_cost(current_node.state, next_node.state)
                    
                    # Format the cost for precise output
                    cost = Decimal(cost).quantize(Decimal('0.000000'))
                    f.write(f"{current_node.state.id} → {next_node.state.id} ({cost})")
                    if i < len(solution) - 2:
                        f.write(", ")
                f.write("]\n")
            else:
                # If no solution was found, indicate this in the output
                f.write("No solution found.\n")


# Main block to execute BFS on a given problem instance
if __name__ == "__main__":
    # Define the file path for input JSON
    json_file_path = '/home/gabri/Inteilligent Systems/src/input/problems/small/plaza_isabel_ii_albacete_250_0.json'
    
    # Create BFS instance
    bfs = BFS(json_file_path)
    
    # Run BFS search and capture the solution if it exists
    solution = bfs.search()

    # Write solution details to output file or print "No solution found"
    if solution:
        output_path = '/home/gabri/Inteilligent Systems/src/output/small/bfs/plaza_isabel_ii_albacete_250_0.txt'
        bfs.write_solution_to_file(solution, output_path)
    else:
        print("No solution found.")
