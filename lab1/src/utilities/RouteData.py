import json
from utilities.State import State
from typing import Any, Dict, List

class RouteData:
    def __init__(self, json_string):
        """
        Initialize RouteData with JSON data, parsing segments and intersections.
        
        Args:
            json_string (str): JSON string containing route data.
        """
        self.data = json.loads(json_string)
        self.segments = self.data.get("segments", [])
        self.intersections = {i["identifier"]: i for i in self.data.get("intersections", [])}

    def get_address(self) -> str:
        """Get address associated with this route data."""
        return self.data.get("address", "No Address")

    def get_distance(self) -> int:
        """Get the distance of the route."""
        return self.data.get("distance", 0)

    def get_initial_final(self) -> Dict[str, int]:
        """Return initial and final node identifiers as a dictionary."""
        return {"initial": self.data.get("initial", 0), "final": self.data.get("final", 0)}

    def get_intersections(self) -> List[Dict[str, Any]]:
        """Get a list of intersections in the data."""
        return list(self.intersections.values())

    def get_segments(self, state_id):
        """Return segments originating from a given state ID."""
        return [segment for segment in self.segments if segment["origin"] == state_id]

    def get_state(self, state_id):
        """Create a State instance based on an intersection ID."""
        intersection = self.intersections.get(state_id)
        if intersection:
            return State(id=state_id, latitude=intersection["latitude"], longitude=intersection["longitude"])
        else:
            raise ValueError(f"No intersection data found for state ID: {state_id}")
