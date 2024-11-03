# search_algorithms/AStarGeodesic.py
import heapq
import math
import time
from decimal import Decimal
from datetime import timedelta
from Search import Search
from utilities.Node import Node
from utilities.State import State

class AStarGeodesic(Search):
    def __init__(self, json_file_path: str):
        super().__init__(json_file_path)
        self.generated_nodes = 0
        self.expanded_nodes = 0
        self.visited = {}

    def search(self):
        start_time = time.time()
        
        frontier = []
        start_node = Node(self.problem.initial_state)
        heapq.heappush(frontier, (self.f(start_node), start_node))
        cost_so_far = {self.problem.initial_state: Decimal(0)}
        self.visited[start_node.state.id] = Decimal(0)

        while frontier:
            f_cost, current_node = heapq.heappop(frontier)
            self.expanded_nodes += 1

            if self.problem.is_goal(current_node.state):
                end_time = time.time()
                return current_node.path(), end_time - start_time

            for action, successor, cost in self.problem.get_successors(current_node.state, include_cost=True):
                new_cost = cost_so_far[current_node.state] + Decimal(cost)

                if successor.id not in self.visited or new_cost < self.visited[successor.id]:
                    self.visited[successor.id] = new_cost
                    cost_so_far[successor] = new_cost
                    priority = new_cost + self.geodesic_heuristic(successor)
                    heapq.heappush(frontier, (priority, Node(successor, current_node, action, float(new_cost))))
                    self.generated_nodes += 1

        return None, time.time() - start_time

    def f(self, node):
        return Decimal(node.path_cost) + self.geodesic_heuristic(node.state)

    def geodesic_heuristic(self, state: State) -> Decimal:
        goal = self.problem.goal_state
        avg_speed = Decimal(120.0)
        
        if state.latitude is None or state.longitude is None or goal.latitude is None or goal.longitude is None:
            return Decimal('inf')

        R = Decimal(6371000)
        lat1, lon1 = Decimal(math.radians(state.latitude)), Decimal(math.radians(state.longitude))
        lat2, lon2 = Decimal(math.radians(goal.latitude)), Decimal(math.radians(goal.longitude))

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = Decimal(math.sin(dlat / 2) ** 2) + Decimal(math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2)
        c = Decimal(2) * Decimal(math.atan2(math.sqrt(a), math.sqrt(1 - a)))
        distance = R * c

        return distance / avg_speed

    def write_solution_to_file(self, solution, execution_time, file_path):
        with open(file_path, 'w') as f:
            if solution:
                f.write(f"Generated nodes: {self.generated_nodes}\n")
                f.write(f"Expanded nodes: {self.expanded_nodes}\n")
                f.write(f"Execution time: {str(timedelta(seconds=execution_time))}\n")
                f.write(f"Solution length: {len(solution) - 1}\n")
                solution_cost = solution[-1].path_cost
                f.write(f"Solution cost: {str(timedelta(seconds=solution_cost))}\n")
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
    astar = AStarGeodesic(json_file_path)
    solution, execution_time = astar.search()

    if solution:
        astar.write_solution_to_file(solution, execution_time, '/home/gabri/Inteilligent Systems/src/output/small/astar_geodesic/plaza_isabel_ii_albacete_250_0.txt')
    else:
        print("No solution found.")
