import json
from typing import List, Tuple, Dict, Any
from utilities.State import State

class RouteData:
    def __init__(self, json_string: str):
        """
        Initialize RouteData with JSON data, parsing segments, intersections, and candidate intersections.

        Args:
            json_string (str): JSON string containing route data.
        """
        self.data = json.loads(json_string)
        self.segments = self.data.get("segments", [])
        self.intersections = {i["identifier"]: i for i in self.data.get("intersections", [])}
        self.candidates = self.data.get("candidates", [])  # List of (identifier, population) tuples
        self.number_stations = self.data.get("number_stations", 0)

        # Cache for precomputed distances
        self.distance_cache = {}

    def get_address(self) -> str:
        """Get the address associated with this route data."""
        return self.data.get("address", "No Address")

    def get_distance(self) -> int:
        """Get the distance of the route."""
        return self.data.get("distance", 0)

    def get_candidates(self) -> List[Tuple[int, int]]:
        """Return the list of candidate intersections and their populations."""
        return self.candidates

    def get_number_stations(self) -> int:
        """Return the number of vehicle stations to locate."""
        return self.number_stations

    def get_intersections(self) -> List[Dict[str, Any]]:
        """Get a list of intersections in the data."""
        return list(self.intersections.values())

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
        from math import radians, sin, cos, sqrt, atan2

        R = 6371  # Radius of Earth in kilometers
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c * 1000  # Convert to meters

    def get_distance_between_intersections(self, id1: int, id2: int) -> float:
        """
        Retrieve or compute the distance between two intersections.

        Args:
            id1 (int): Identifier for the first intersection.
            id2 (int): Identifier for the second intersection.

        Returns:
            float: Distance in meters.
        """
        if (id1, id2) in self.distance_cache:
            return self.distance_cache[(id1, id2)]

        intersection1 = self.intersections.get(id1)
        intersection2 = self.intersections.get(id2)

        if not intersection1 or not intersection2:
            raise ValueError(f"Invalid intersection IDs: {id1}, {id2}")

        lat1, lon1 = intersection1["latitude"], intersection1["longitude"]
        lat2, lon2 = intersection2["latitude"], intersection2["longitude"]
        
        distance = self.compute_haversine(lat1, lon1, lat2, lon2)
        self.distance_cache[(id1, id2)] = distance
        self.distance_cache[(id2, id1)] = distance  # Symmetric caching
        return distance

    def validate_segments(self) -> bool:
        """
        Validate if all segments have valid origins and destinations.

        Returns:
            bool: True if valid, False otherwise.
        """
        for segment in self.segments:
            if segment["origin"] not in self.intersections or segment["destination"] not in self.intersections:
                return False
        return True

    def validate_candidates(self) -> bool:
        """
        Validate if all candidates are valid intersections.

        Returns:
            bool: True if valid, False otherwise.
        """
        for candidate_id, _ in self.candidates:
            if candidate_id not in self.intersections:
                return False
        return True

    def validate_data(self) -> bool:
        """
        Validate the overall consistency of the route data.

        Returns:
            bool: True if all validations pass, False otherwise.
        """
        return self.validate_segments() and self.validate_candidates()

    def get_segments(self, state_id: int) -> List[Dict[str, Any]]:
        """
        Return segments originating from a given state ID.

        Args:
            state_id (int): State ID to retrieve segments for.

        Returns:
            List[Dict[str, Any]]: List of segment dictionaries.
        """
        return [segment for segment in self.segments if segment["origin"] == state_id]

    def get_state(self, state_id: int) -> State:
        """
        Create a State instance based on an intersection ID.

        Args:
            state_id (int): Intersection ID to create a state for.

        Returns:
            State: State object corresponding to the intersection.
        """
        intersection = self.intersections.get(state_id)
        if intersection:
            return State(id=state_id, latitude=intersection["latitude"], longitude=intersection["longitude"])
        else:
            raise ValueError(f"No intersection data found for state ID: {state_id}")
