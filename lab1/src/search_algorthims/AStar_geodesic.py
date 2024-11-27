# A* Search with Geodesic Heuristic

import heapq
import math
import time
from decimal import Decimal
from datetime import timedelta
from Search import Search
from utilities.Node import Node
from utilities.State import State

# This class implements the A* algorithm using a geodesic (Haversine) heuristic to calculate 
# the straight-line distance between two points on the Earth’s surface.
class AStarGeodesic(Search):
    def __init__(self, json_file_path: str):
        super().__init__(json_file_path)
        self.generated_nodes = 0  # Tracks nodes added to the frontier
        self.expanded_nodes = 0   # Tracks nodes that have been expanded
        self.visited = {}         # Dictionary to store visited nodes and their costs

    def search(self):
        # Start timing the search
        start_time = time.time()
        
        # Priority queue (frontier) for A* algorithm, starting with the initial state
        frontier = []
        start_node = Node(self.problem.initial_state)
        
        # Push initial node to the frontier with its priority (f-cost)
        heapq.heappush(frontier, (self.f(start_node), start_node))
        
        # Track cost from the start to each node
        cost_so_far = {self.problem.initial_state: Decimal(0)}
        self.visited[start_node.state.id] = Decimal(0)

        while frontier:
            # Pop node with the lowest f-cost
            f_cost, current_node = heapq.heappop(frontier)
            self.expanded_nodes += 1

            # Check if we've reached the goal
            if self.problem.is_goal(current_node.state):
                end_time = time.time()
                return current_node.path(), end_time - start_time

            # Explore each successor of the current node
            for action, successor, cost in self.problem.get_successors(current_node.state, include_cost=True):
                new_cost = cost_so_far[current_node.state] + Decimal(cost)  # g(n)

                # Only proceed if we have not visited this successor or found a cheaper path
                if successor.id not in self.visited or new_cost < self.visited[successor.id]:
                    self.visited[successor.id] = new_cost
                    cost_so_far[successor] = new_cost
                    priority = new_cost + self.geodesic_heuristic(successor)  # f(n) = g(n) + h(n)
                    
                    # Add successor to the frontier with calculated priority
                    heapq.heappush(frontier, (priority, Node(successor, current_node, action, float(new_cost))))
                    self.generated_nodes += 1  # Increment generated node count

        # If no solution found, return None and the time taken
        return None, time.time() - start_time

    def f(self, node):
        # Calculates the f-cost for a node: g(n) + h(n)
        return Decimal(node.path_cost) + self.geodesic_heuristic(node.state)

    def geodesic_heuristic(self, state: State) -> Decimal:
        # This heuristic calculates the straight-line (geodesic) distance to the goal using the Haversine formula.
        goal = self.problem.goal_state
        avg_speed = Decimal(120.0)  # Speed in meters/second to estimate travel time
        
        # If coordinates are missing, return infinity to avoid this path
        if state.latitude is None or state.longitude is None or goal.latitude is None or goal.longitude is None:
            return Decimal('inf')

        # Radius of Earth (in meters)
        R = Decimal(6371000)
        lat1, lon1 = Decimal(math.radians(state.latitude)), Decimal(math.radians(state.longitude))
        lat2, lon2 = Decimal(math.radians(goal.latitude)), Decimal(math.radians(goal.longitude))

        # Haversine formula to calculate the distance
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = Decimal(math.sin(dlat / 2) ** 2) + Decimal(math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2)
        c = Decimal(2) * Decimal(math.atan2(math.sqrt(a), math.sqrt(1 - a)))
        distance = R * c

        # Estimated travel time to the goal
        return distance / avg_speed

    def write_solution_to_file(self, solution, execution_time, file_path):
        # This function writes the solution and various metrics to a file for analysis.
        with open(file_path, 'w') as f:
            if solution:
                # Write general metrics
                f.write(f"Generated nodes: {self.generated_nodes}\n")
                f.write(f"Expanded nodes: {self.expanded_nodes}\n")
                f.write(f"Execution time: {str(timedelta(seconds=execution_time))}\n")
                f.write(f"Solution length: {len(solution) - 1}\n")
                
                # Write the cost of the entire solution path
                solution_cost = solution[-1].path_cost
                f.write(f"Solution cost: {str(timedelta(seconds=solution_cost))}\n")
                
                # Write the solution path
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

# Main section for testing and running the algorithm
if __name__ == "__main__":
    # Load a problem from JSON and run A* Geodesic search
    json_file_path = '/home/gabri/Inteilligent Systems/src/input/problems/huge/calle_cardenal_tabera_y_araoz_albacete_2000_1.json'
    astar = AStarGeodesic(json_file_path)
    
    # Run the search and obtain the solution and execution time
    solution, execution_time = astar.search()

    # Write solution to output file or print "No solution found"
    if solution:
        astar.write_solution_to_file(solution, execution_time, '/home/gabri/Inteilligent Systems/src/output/huge/astar_geodesic/plaza_isabel_ii_albacete_250_0.txt')
    else:
        print("No solution found.")
