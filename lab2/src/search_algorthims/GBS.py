import heapq
import math
import time
from datetime import timedelta
from decimal import Decimal, getcontext
from Search import Search
from utilities.Node import Node
from utilities.State import State

# Set precision for Decimal calculations
getcontext().prec = 20

# Greedy Best-First Search using Geodesic (Haversine) heuristic
class GreedyBestGeodesic(Search):
    def __init__(self, json_file_path: str):
        # Initialize with tracking variables for nodes generated and expanded
        super().__init__(json_file_path)
        self.generated_nodes = 0
        self.expanded_nodes = 0

    def search(self):
        """Execute Greedy Best-First Search using only the geodesic heuristic for node ordering."""
        
        # Start tracking execution time
        start_time = time.time()
        
        # Initialize priority queue (frontier) and add the start node
        frontier = []
        start_node = Node(self.problem.initial_state)
        heapq.heappush(frontier, (self.geodesic_heuristic(start_node.state), start_node))
        self.checked.add(start_node.state)  # Track explored nodes

        while frontier:
            # Pop node with the lowest heuristic value
            _, current_node = heapq.heappop(frontier)
            self.expanded_nodes += 1

            print(f"Exploring: {current_node.state}")

            # Check if the current node is the goal
            if self.problem.is_goal(current_node.state):
                end_time = time.time()
                print("Goal found!")
                execution_time = end_time - start_time
                return current_node.path(), execution_time

            # Expand current node, adding successors to the frontier if not explored
            for action, successor, cost in self.problem.get_successors(current_node.state, include_cost=True):
                if successor not in self.checked:
                    self.checked.add(successor)
                    priority = self.geodesic_heuristic(successor)  # Use heuristic value for ordering
                    heapq.heappush(frontier, (priority, Node(successor, current_node, action, current_node.path_cost + cost)))
                    self.generated_nodes += 1
                    print(f"Adding to frontier: {successor}")

        print("No solution found.")
        return None, 0

    def geodesic_heuristic(self, state: State) -> float:
        """Calculate the geodesic distance (using Haversine formula) to approximate travel time to the goal."""
        
        goal = self.problem.goal_state
        avg_speed = Decimal(120.0)  # Tuned average speed in meters per second
        
        # Return high cost if coordinates are missing
        if state.latitude is None or state.longitude is None or goal.latitude is None or goal.longitude is None:
            return float('inf')

        # Haversine formula to calculate the straight-line distance
        R = Decimal(6371000)  # Earth radius in meters
        lat1 = Decimal(math.radians(state.latitude))
        lon1 = Decimal(math.radians(state.longitude))
        lat2 = Decimal(math.radians(goal.latitude))
        lon2 = Decimal(math.radians(goal.longitude))

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = Decimal(math.sin(dlat / 2) ** 2) + Decimal(math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2)
        c = Decimal(2) * Decimal(math.atan2(math.sqrt(a), math.sqrt(1 - a)))
        distance = R * c  # Calculate distance in meters

        # Scale the distance by average speed to estimate travel time
        return (distance / avg_speed).quantize(Decimal('0.000000'))

    def write_solution_to_file(self, solution, execution_time, file_path):
        """Write the solution path and search metrics to a file for analysis."""
        
        with open(file_path, 'w') as f:
            if solution:
                # Write out statistics about nodes
                f.write(f"Generated nodes: {self.generated_nodes}\n")
                f.write(f"Expanded nodes: {self.expanded_nodes}\n")
                
                # Format execution time as a timedelta for expected output
                f.write(f"Execution time: {str(timedelta(seconds=execution_time))}\n")
                
                # Record solution length
                f.write(f"Solution length: {len(solution) - 1}\n")
                
                # Write solution path cost, formatted for precision
                solution_cost = solution[-1].path_cost
                formatted_cost = str(timedelta(seconds=solution_cost))
                f.write(f"Solution cost: {formatted_cost}\n")
                
                # Write each step in the solution path
                f.write("Solution: [")
                
                for i in range(len(solution) - 1):
                    current_node = solution[i]
                    next_node = solution[i + 1]
                    action, cost = self.problem.get_action_and_cost(current_node.state, next_node.state)
                    cost = Decimal(cost).quantize(Decimal('0.000000'))  # Ensure six decimal places for cost
                    f.write(f"{current_node.state.id} → {next_node.state.id} ({cost})")
                    if i < len(solution) - 2:
                        f.write(", ")
                f.write("]\n")
            else:
                # Indicate that no solution was found
                f.write("No solution found.\n")

# Main function to execute the Greedy Best-First Search
if __name__ == "__main__":
    # Define path to input JSON file
    json_file_path = '/home/gabri/Inteilligent Systems/src/input/problems/huge/calle_cardenal_tabera_y_araoz_albacete_2000_1.json'
    
    # Create a GreedyBestGeodesic instance and start the search
    greedy_search = GreedyBestGeodesic(json_file_path)
    solution, execution_time = greedy_search.search()
    
    # Write the solution to an output file if found
    if solution:
        output_path = '/home/gabri/Inteilligent Systems/src/output/huge/gbs/plaza_isabel_ii_albacete_250_0.txt'
        greedy_search.write_solution_to_file(solution, execution_time, output_path)
    else:
        print("No solution found.")
