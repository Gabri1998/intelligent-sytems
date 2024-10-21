import heapq
import time
from typing import Any,Dict, List, Tuple
from Search import Search
from utilities.Node import Node
from utilities.State import State
from utilities.RouteData import RouteData

class AStar(Search):
    def __init__(self, json_file_path: str, heuristic):
        super().__init__(json_file_path)
        self.heuristic = heuristic
        self.generated_nodes = 0
        self.expanded_nodes = 0
        self.execution_time = 0

    # Override the build_graph method to include coordinates for A*
    def build_graph(self, route_data: RouteData) -> Dict[int, List[Tuple[str, State, float]]]:
        """Builds the graph using the segments from RouteData with coordinates."""
        graph = {}
        intersections = {i["identifier"]: (i["latitude"], i["longitude"]) for i in route_data.get_intersections()}
        
        for segment in route_data.get_segments():
            origin = segment["origin"]
            destination = segment["destination"]
            distance = segment["distance"]
            
            origin_lat, origin_lon = intersections.get(origin, (None, None))
            dest_lat, dest_lon = intersections.get(destination, (None, None))
            
            # Add bidirectional segments with States containing coordinates
            if origin not in graph:
                graph[origin] = []
            graph[origin].append((f"move to {destination}", State(destination, dest_lat, dest_lon), distance))
            
            if destination not in graph:
                graph[destination] = []
            graph[destination].append((f"move to {origin}", State(origin, origin_lat, origin_lon), distance))
        
        return graph

    def search(self):
        """Perform the A* search."""
        start_time = time.time()
        frontier = []
        start_node = Node(self.problem.initial_state)
        heapq.heappush(frontier, (self.f(start_node), start_node))
        self.checked = set()
        cost_so_far = {self.problem.initial_state: 0}

        while frontier:
            f_cost, node = heapq.heappop(frontier)
            print(f"Exploring: {node.state}")
            self.expanded_nodes += 1

            if self.problem.is_goal(node.state):
                end_time = time.time()
                self.execution_time = end_time - start_time
                self.solution_cost = node.path_cost
                print("Goal found!")
                return node.path()

            self.checked.add(node.state)

            for child in node.expand(self.problem):
                new_cost = node.path_cost + self.problem.step_cost(node.state, child.action, child.state)
                
                if child.state not in cost_so_far or new_cost < cost_so_far[child.state]:
                    cost_so_far[child.state] = new_cost
                    priority = new_cost + self.heuristic(child.state)
                    heapq.heappush(frontier, (priority, child))
                    self.generated_nodes += 1

        end_time = time.time()
        self.execution_time = end_time - start_time
        print("No solution found.")
        return None

    def f(self, node):
        """f(n) = g(n) + h(n): Path cost plus heuristic estimate to goal."""
        return node.path_cost + self.heuristic(node.state)

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
    def manhattan_heuristic(state, goal_state):
        """Manhattan distance heuristic for grid-based problems."""
        return abs(state.latitude - goal_state.latitude) + abs(state.longitude - goal_state.longitude)

    json_file_path = '/home/gabri/Inteilligent Systems/src/input/problems/small/plaza_isabel_ii_albacete_250_0.json'
    astar = AStar(json_file_path, lambda state: manhattan_heuristic(state, astar.problem.goal_state))
    solution = astar.search()

    if solution:
        astar.write_solution_to_file(solution, '/home/gabri/Inteilligent Systems/src/output/small/astar/plaza_isabel_ii_albacete_250_0.txt')
    else:
        print("No solution found.")
