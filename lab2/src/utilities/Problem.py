from typing import List, Tuple, Dict
from utilities.State import State
from utilities.RouteData import RouteData
import random
from math import radians, sin, cos, sqrt, atan2

class Problem:
    def __init__(self, route_data: RouteData):
        """
        Initialize the Problem instance for Lab 2.

        Args:
            route_data (RouteData): Parsed route data object.
        """
        self.route_data = route_data
        self.intersections = route_data.get_intersections()
        self.candidates = route_data.get_candidates()  # (id, population)
        self.candidate_intersections = [candidate[0] for candidate in self.candidates]
        self.number_stations = route_data.get_number_stations()

        # Caches for travel time and fitness evaluation
        self.travel_time_cache = {}
        self.evaluation_cache = {}

    def compute_travel_time(self, state1: State, state2: State) -> float:
        """
        Compute the travel time between two states using a heuristic.

        Args:
            state1 (State): The starting state.
            state2 (State): The destination state.

        Returns:
            float: The travel time in seconds.
        """
        if (state1.id, state2.id) in self.travel_time_cache:
            return self.travel_time_cache[(state1.id, state2.id)]

        # Use haversine distance as the heuristic
        distance = self.compute_haversine(state1.latitude, state1.longitude, state2.latitude, state2.longitude)
        travel_time = (distance / 50) * 3.6  # Assuming average speed of 50 km/h

        # Cache the computed travel time
        self.travel_time_cache[(state1.id, state2.id)] = travel_time
        return travel_time

    def evaluate_solution(self, chromosome: List[int]) -> float:
        """
        Evaluate the fitness of a given solution (chromosome).

        Args:
            chromosome (List[int]): The chromosome representing the solution.

        Returns:
            float: The fitness score (lower is better).
        """
        config_tuple = tuple(chromosome)
        if config_tuple in self.evaluation_cache:
            return self.evaluation_cache[config_tuple]

        if sum(chromosome) != self.number_stations:
            raise ValueError(
                f"Invalid configuration: Expected {self.number_stations} active stations but got {sum(chromosome)}."
            )

        total_population = sum(pop for _, pop in self.candidates)
        weighted_travel_time = 0.0

        for candidate_id, population in self.candidates:
            candidate_state = self.route_data.get_state(candidate_id)
            min_travel_time = float('inf')

            for station_id, active in enumerate(chromosome):
                if active:
                    station_state = self.route_data.get_state(self.candidate_intersections[station_id])
                    travel_time = self.compute_travel_time(candidate_state, station_state)
                    min_travel_time = min(min_travel_time, travel_time)

            if min_travel_time == float('inf'):
                min_travel_time = 18000  # Fallback for unreachable candidates

            weighted_travel_time += population * min_travel_time

        fitness = weighted_travel_time / total_population
        self.evaluation_cache[config_tuple] = fitness
        return fitness

    def generate_random_chromosome(self) -> List[int]:
        """
        Generate a random chromosome representing a possible solution.

        Returns:
            List[int]: A chromosome with random active stations.
        """
        chromosome = [0] * len(self.candidates)
        active_indices = random.sample(range(len(chromosome)), self.number_stations)
        for idx in active_indices:
            chromosome[idx] = 1
        return chromosome

    def compute_haversine(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Compute the haversine distance between two geographic points.

        Args:
            lat1 (float): Latitude of point 1.
            lon1 (float): Longitude of point 1.
            lat2 (float): Latitude of point 2.
            lon2 (float): Longitude of point 2.

        Returns:
            float: Distance in meters.
        """
        R = 6371  # Radius of Earth in kilometers
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c * 1000  # Convert to meters

    def fix_chromosome(self, chromosome: List[int]) -> List[int]:
        """
        Fix a chromosome to ensure it has the correct number of active stations.

        Args:
            chromosome (List[int]): The chromosome to fix.

        Returns:
            List[int]: The fixed chromosome.
        """
        active_positions = [i for i, gene in enumerate(chromosome) if gene == 1]
        if len(active_positions) > self.number_stations:
            excess = random.sample(active_positions, len(active_positions) - self.number_stations)
            for idx in excess:
                chromosome[idx] = 0
        elif len(active_positions) < self.number_stations:
            inactive_positions = [i for i, gene in enumerate(chromosome) if gene == 0]
            additions = random.sample(inactive_positions, self.number_stations - len(active_positions))
            for idx in additions:
                chromosome[idx] = 1
        return chromosome

    def validate_chromosome(self, chromosome: List[int]) -> bool:
        """
        Validate if a chromosome has the correct number of active stations.

        Args:
            chromosome (List[int]): The chromosome to validate.

        Returns:
            bool: True if valid, False otherwise.
        """
        return sum(chromosome) == self.number_stations
