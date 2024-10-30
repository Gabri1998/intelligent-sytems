import heapq
import time  
from Search import Search
from utilities.Node import Node


class UCS(Search):
    def __init__(self, json_file_path: str):
        super().__init__(json_file_path)  # Inherit from the Search class
        self.generated_nodes = 0
        self.expanded_nodes = 0
        self.execution_time = 0

    def search(self):
        """Perform the UCS search."""
        start_time = time.time()  # Start tracking time
        frontier = []  # Priority queue (min-heap)
        heapq.heappush(frontier, (0, Node(self.problem.initial_state)))  # Add initial state with cost 0
        self.checked = set()  # Explored nodes

        # Cost dictionary to keep track of the lowest cost to reach each state
        cost_so_far = {self.problem.initial_state: 0}

        while frontier:
            current_cost, node = heapq.heappop(frontier)  # Pop the node with the lowest path cost
            print(f"Exploring: {node.state}")
            self.expanded_nodes += 1  # Increment expanded nodes count

            # Check if we've reached the goal
            if self.problem.is_goal(node.state):
                end_time = time.time()  # Stop tracking time
                self.execution_time = end_time - start_time  # Calculate execution time
                self.solution_cost = current_cost  # Total solution cost
                print("Goal found!")
                return node.path()  # Return the path to the goal

            # Mark the node as explored
            self.checked.add(node.state)

            # Expand the node
            for child in node.expand(self.problem):
                new_cost = current_cost + self.problem.step_cost(node.state, child.action, child.state)
                if child.state not in cost_so_far or new_cost < cost_so_far[child.state]:
                    cost_so_far[child.state] = new_cost
                    heapq.heappush(frontier, (new_cost, child))  # Add child with its new cost
                    self.generated_nodes += 1  # Increment generated nodes count
                    print(f"Adding to frontier: {child.state}, cost: {new_cost}")

        end_time = time.time()  # Stop tracking time
        self.execution_time = end_time - start_time  # Calculate execution time
        print("No solution found after exploring all states.")
        return None

    def write_solution_to_file(self, solution, file_path):
        """Write the solution path and additional information to a text file."""
        with open(file_path, 'w') as f:
            if solution:
                f.write(f"Generated nodes: {self.generated_nodes}\n")
                f.write(f"Expanded nodes: {self.expanded_nodes}\n")
                f.write(f"Execution time: {self.execution_time}\n")
                f.write(f"Solution length: {len(solution) - 1}\n")
                f.write(f"Solution cost: {self.solution_cost}\n")
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
    ucs = UCS(json_file_path)
    solution = ucs.search()  # Call the search method

    if solution:
        ucs.write_solution_to_file(solution,
                                   '/home/gabri/Inteilligent Systems/src/output/small/ucs/plaza_isabel_ii_albacete_250_0.txt')  # Write solution to file
    else:
        print("No solution found.")
