import os
import time  # Import time for execution time tracking
from collections import deque
from Search import Search
from Node import Node


class BFS(Search):
    def __init__(self, json_file_path: str):
        super().__init__(json_file_path)
        self.generated_nodes = 0
        self.expanded_nodes = 0

    def search(self):
        """Perform the BFS search."""
        start_time = time.time()  # Start tracking time
        frontier = deque([Node(self.problem.initial_state)])
        self.checked = {self.problem.initial_state}

        while frontier:
            node = frontier.popleft()  # Pop the first node in the queue (BFS behavior)
            print(f"Exploring: {node.state}")
            self.expanded_nodes += 1  # Increment expanded nodes count

            if self.problem.is_goal(node.state):
                end_time = time.time()  # Stop tracking time
                self.execution_time = end_time - start_time  # Calculate execution time
                self.solution_cost = node.path_cost  # Total solution cost
                print("Goal found!")
                return node.path()  # Return the path to the goal

            for child in node.expand(self.problem):
                if child.state not in self.checked:
                    frontier.append(child)
                    self.checked.add(child.state)
                    self.generated_nodes += 1  # Increment generated nodes count
                    print(f"Adding to frontier: {child.state}")

        end_time = time.time()  # Stop tracking time
        self.execution_time = end_time - start_time  # Calculate execution time
        print("No solution found after exploring all states.")
        return None

    def write_solution_to_file(self, solution, file_path):
        """Write the solution path and additional information to a text file."""
        with open(file_path, 'w', encoding="utf-8") as f:
            if solution:
                # Writing the solution path and costs
                for i in range(len(solution) - 1):
                    current_node = solution[i]
                    next_node = solution[i + 1]
                    action, cost = self.problem.get_action_and_cost(current_node.state, next_node.state)
                    f.write(f"{current_node.state.id} → {next_node.state.id}, {cost}\n")

                # Writing additional metadata (generated nodes, expanded nodes, etc.)
                f.write(f"Generated nodes: {self.generated_nodes}\n")
                f.write(f"Expanded nodes: {self.expanded_nodes}\n")
                f.write(f"Execution time: {self.execution_time}\n")
                f.write(f"Solution length: {len(solution) - 1}\n")
                f.write(f"Solution cost: {self.solution_cost}\n")
            else:
                f.write("No solution found.\n")


if __name__ == "__main__":
    json_file_path = r'C:\Users\obada\Desktop\Courses This Semester\Intelligent Systems\intelligent-sytems\src\input\problems\small\plaza_isabel_ii_albacete_250_0.json'
    bfs = BFS(json_file_path)
    solution = bfs.search()  # Call the search method

    if solution:
        bfs.write_solution_to_file(solution,
                                   r'C:\Users\obada\Desktop\Courses This Semester\Intelligent Systems\intelligent-sytems\src\output\plaza_isabel_ii_albacete_250_0.txt')  # Write solution to file
    else:
        print("No solution found.")
